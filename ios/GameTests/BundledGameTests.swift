import WebKit
import XCTest
@testable import MakeSomething

@MainActor
final class BundledGameTests: XCTestCase {
    private func wait(_ script: String, in game: GameWebView) async throws {
        let deadline = Date().addingTimeInterval(15)
        while Date() < deadline {
            if (try? await game.evaluateJavaScript(script)) as? Bool == true { return }
            try await Task.sleep(nanoseconds: 100_000_000)
        }
        let state = try? await game.evaluateJavaScript("[location.href, document.referrer, document.body.innerText.slice(0, 300)].join(' | ')")
        print("Timed out: \(script); \(state ?? "")")
        throw NSError(domain: "BundledGame", code: 1, userInfo: [
            NSLocalizedDescriptionKey: "Timed out waiting for \(script). Page: \(state ?? "")"
        ])
    }

    func testProductionCatalogueAndBoards() async throws {
        let game = GameWebView(dataStore: .nonPersistent())
        let scene = try XCTUnwrap(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
        let window = UIWindow(windowScene: scene)
        window.rootViewController = UIViewController()
        window.rootViewController?.view = game
        window.makeKeyAndVisible()
        defer { window.isHidden = true }
        game.openCatalogue()
        try await wait("!!document.querySelector('link[rel=manifest]')", in: game)
        let links = try await game.evaluateJavaScript("Array.from(document.querySelectorAll('a[data-story]'), a => a.href)")
        let urls = try XCTUnwrap(links as? [String])
        XCTAssertFalse(urls.isEmpty)
        for address in urls {
            game.load(URLRequest(url: try XCTUnwrap(URL(string: address))))
            try await wait("!!document.querySelector('.story-start')", in: game)
            _ = try await game.evaluateJavaScript("document.querySelector('.story-start').click()")
            try await wait("!!document.querySelector('dialog[open] button')", in: game)
            _ = try await game.evaluateJavaScript("document.querySelector('dialog[open] button').click()")
            try await wait("!!document.querySelector('[data-item]') && !document.querySelector('.debug-toggle')", in: game)
        }
    }

    func testCatalogueHandoffWorkerStorageAndCitation() async throws {
        let store = WKWebsiteDataStore.nonPersistent()
        let citation = expectation(description: "Hand citation to iOS once")
        citation.assertForOverFulfill = true
        let scene = try XCTUnwrap(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
        let window = UIWindow(windowScene: scene)
        let controller = UIViewController()
        window.rootViewController = controller
        var game = GameWebView(dataStore: store) { url in
            XCTAssertEqual(url.absoluteString, "https://example.org/reading")
            citation.fulfill()
        }
        controller.view = game
        window.makeKeyAndVisible()
        defer { window.isHidden = true }
        game.openCatalogue()
        try await wait("!!document.querySelector('link[rel=manifest]')", in: game)
        _ = try await game.evaluateJavaScript("document.querySelector('a[data-story]').click()")
        try await wait("!!document.querySelector('dialog[open] button')", in: game)
        _ = try await game.evaluateJavaScript("document.querySelector('dialog[open] button').click()")
        try await wait("!document.querySelector('[data-story-flip]')", in: game)
        _ = try await game.evaluateJavaScript("document.querySelector('[data-command=story]').click()")
        try await wait("!!document.querySelector('.popup-home')", in: game)

        // Exercise module-worker delivery, including its imports, from the installed bundle.
        let workerReply = try await game.callAsyncJavaScript("""
            const files = await (await fetch('./assets/build-files.json')).json();
            const worker = new Worker(files.find(f => f.includes('/goal-worker-')), {type:'module'});
            return await new Promise((resolve, reject) => {
              worker.onmessage = () => { worker.terminate(); resolve(true); };
              worker.onerror = e => reject(Error(e.message || 'Worker failed to load'));
              worker.postMessage({});
              setTimeout(() => { worker.terminate(); reject(Error('Worker timed out')); }, 5000);
            });
            """, arguments: [:], in: nil, contentWorld: .page)
        XCTAssertEqual(workerReply as? Bool, true)
        let remoteBlocked = try await game.callAsyncJavaScript("""
            return await new Promise(resolve => {
              document.addEventListener('securitypolicyviolation', e => {
                resolve(e.blockedURI.includes('example.invalid'));
              }, {once:true});
              fetch('https://example.invalid').catch(() => {});
              setTimeout(() => resolve(false), 3000);
            });
            """, arguments: [:], in: nil, contentWorld: .page)
        XCTAssertEqual(remoteBlocked as? Bool, true)

        _ = try await game.evaluateJavaScript("""
            localStorage.setItem('persistence-test', 'saved');
            const a = document.createElement('a');
            a.href='https://example.org/reading'; a.target='_blank'; a.rel='noopener noreferrer';
            document.body.append(a); a.click();
            """)
        await fulfillment(of: [citation], timeout: 3)
        XCTAssertEqual(game.url?.path, "/make-something.html")
        _ = try await game.evaluateJavaScript("document.querySelector('.popup-home').click()")
        try await wait("!!document.querySelector('a[data-story]')", in: game)
        game = GameWebView(dataStore: store)
        controller.view = game
        game.openCatalogue()
        try await wait("localStorage.getItem('persistence-test') === 'saved'", in: game)
    }
}
