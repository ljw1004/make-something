import WebKit
import XCTest
@testable import MakeSomething

@MainActor
final class BundledGameTests: XCTestCase {
    private func findGame(in view: UIView) -> GameWebView? {
        if let game = view as? GameWebView { return game }
        return view.subviews.lazy.compactMap { self.findGame(in: $0) }.first
    }

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

    func testNativeArtworkAndStatusBarBlurUseTheWindowEdges() async throws {
        let scene = try XCTUnwrap(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
        let game = try XCTUnwrap(scene.windows.lazy.compactMap { self.findGame(in: $0) }.first)
        try await wait("!!document.querySelector('.carousel-art')?.naturalWidth", in: game)
        let window = try XCTUnwrap(game.window)
        XCTAssertEqual(game.convert(game.bounds, to: window), window.bounds)

        let viewport = try await game.evaluateJavaScript("""
            (() => {
              const blur = document.querySelector('.status-bar-color');
              const rect = blur.getBoundingClientRect();
              const style = getComputedStyle(blur);
              const surface = document.querySelector('#catalogue-app').getBoundingClientRect();
              const slide = document.querySelector('.carousel-slide:not([hidden])');
              const footer = slide.querySelector('.carousel-footer').getBoundingClientRect();
              const subtitleSize = getComputedStyle(slide.querySelector('.carousel-description')).fontSize;
              const footerSizes = Array.from(slide.querySelectorAll('.carousel-footer a'), link => getComputedStyle(link).fontSize);
              return {surfaceHeight: surface.height, blurTop: rect.top, blurBottom: rect.bottom,
                      blurWidth: rect.width, filter: style.backdropFilter || style.webkitBackdropFilter,
                      mask: style.maskImage, pointerEvents: style.pointerEvents,
                      footerHeight: footer.height, footerInset: surface.bottom - footer.bottom,
                      subtitleSize, footerSizes};
            })()
            """)
        let layout = try XCTUnwrap(viewport as? [String: Any])
        XCTAssertEqual(try XCTUnwrap(layout["surfaceHeight"] as? CGFloat), window.bounds.height, accuracy: 1)
        XCTAssertEqual(layout["blurTop"] as? CGFloat, 0)
        XCTAssertEqual(try XCTUnwrap(layout["blurBottom"] as? CGFloat), window.safeAreaInsets.top, accuracy: 1)
        XCTAssertEqual(try XCTUnwrap(layout["blurWidth"] as? CGFloat), window.bounds.width, accuracy: 1)
        XCTAssertEqual(layout["filter"] as? String, "blur(1px)")
        XCTAssertTrue((layout["mask"] as? String)?.hasPrefix("linear-gradient(") == true)
        XCTAssertEqual(layout["pointerEvents"] as? String, "none")
        XCTAssertGreaterThanOrEqual(try XCTUnwrap(layout["footerHeight"] as? CGFloat), 44)
        XCTAssertGreaterThanOrEqual(try XCTUnwrap(layout["footerInset"] as? CGFloat), window.safeAreaInsets.bottom + 3)
        let subtitleSize = try XCTUnwrap(layout["subtitleSize"] as? String)
        XCTAssertEqual(layout["footerSizes"] as? [String], [subtitleSize, subtitleSize])
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
        for title in ["Cookbook", "Settlement"] {
            _ = try await game.evaluateJavaScript("document.querySelector('.carousel-slide:not([hidden]) .carousel-dots button[aria-label=\(title)]').click()")
            try await wait("""
                (() => {
                  const card = document.querySelector('.carousel-slide:not([hidden])');
                  return card?.ariaLabel === '\(title)' && card.dataset.ink === 'dark' &&
                    Array.from(card.querySelectorAll('.carousel-description, .carousel-footer a'), label =>
                      getComputedStyle(label).color).join('|') === 'rgb(0, 0, 0)|rgb(0, 0, 0)|rgb(0, 0, 0)';
                })()
                """, in: game)
        }
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

    func testCatalogueHandoffWorkerStorageAndExternalLinks() async throws {
        let store = WKWebsiteDataStore.nonPersistent()
        let support = expectation(description: "Hand support link to iOS once")
        let privacy = expectation(description: "Hand privacy link to iOS once")
        let citation = expectation(description: "Hand citation to iOS once")
        [support, privacy, citation].forEach { $0.assertForOverFulfill = true }
        let scene = try XCTUnwrap(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
        let window = UIWindow(windowScene: scene)
        let controller = UIViewController()
        window.rootViewController = controller
        var game = GameWebView(dataStore: store) { url in
            switch url.absoluteString {
            case "https://unto.me/make-something/support.html": support.fulfill()
            case "https://unto.me/make-something/privacy.html": privacy.fulfill()
            case "https://example.org/reading": citation.fulfill()
            default: XCTFail("Unexpected external URL: \(url)")
            }
        }
        controller.view = game
        window.makeKeyAndVisible()
        defer { window.isHidden = true }
        game.openCatalogue()
        try await wait("!!document.querySelector('.carousel-slide:not([hidden]) .carousel-footer:not([hidden])')", in: game)
        _ = try await game.evaluateJavaScript("document.querySelectorAll('.carousel-slide:not([hidden]) .carousel-footer a').forEach(link => link.click())")
        await fulfillment(of: [support, privacy], timeout: 3)
        XCTAssertEqual(game.url, BundledWebsite.catalogue)
        // Observe the actual embedded worker while the opening board ranks its goals.
        _ = try await game.evaluateJavaScript("""
            const NativeWorker = Worker;
            let workerProbe;
            window.workerResult = 'No goal worker constructed';
            window.Worker = class extends NativeWorker {
              constructor(url, options) {
                if (!workerProbe) {
                  window.workerResult = 'Loading ' + String(url).split(':')[0] + ' worker';
                  try {
                    // The game can cancel a search after 250ms. Give this independent
                    // copy of its real worker time to start on a cold simulator.
                    workerProbe = new NativeWorker(url, options);
                    workerProbe.onmessage = () => { window.workerResult = 'ready'; workerProbe.terminate(); };
                    workerProbe.onerror = e => { window.workerResult = e.message || 'Worker load failed'; };
                    workerProbe.postMessage({});
                  } catch (error) { window.workerResult = String(error); }
                }
                super(url, options);
              }
            };
            true
            """)
        _ = try await game.evaluateJavaScript("document.querySelector('a[data-story]').click()")
        try await wait("!!document.querySelector('dialog[open] button')", in: game)
        _ = try await game.evaluateJavaScript("document.querySelector('dialog[open] button').click()")
        try await wait("""
            (() => {
              const board = document.querySelector('.game-surface');
              return !!board && !board.inert && board.getBoundingClientRect().top === 0;
            })()
            """, in: game)
        _ = try await game.evaluateJavaScript("document.querySelector('[data-command=story]').click()")
        try await wait("!!document.querySelector('.popup-home')", in: game)

        do {
            try await wait("window.workerResult === 'ready'", in: game)
        } catch {
            let detail = try await game.evaluateJavaScript("window.workerResult")
            XCTFail("Embedded worker failed: \(String(describing: detail))")
        }
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
        XCTAssertEqual(game.url?.path, "/index.html")
        _ = try await game.evaluateJavaScript("document.querySelector('.popup-home').click()")
        try await wait("location.pathname === '/index.html' && !document.querySelector('.game-surface')", in: game)
        game = GameWebView(dataStore: store)
        controller.view = game
        game.openCatalogue()
        try await wait("localStorage.getItem('persistence-test') === 'saved'", in: game)
    }
}
