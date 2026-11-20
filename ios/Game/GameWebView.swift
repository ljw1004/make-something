import UIKit
import WebKit

private final class CombinationHaptics: NSObject, WKScriptMessageHandler {
    private static let enabledKey = "combinationHapticsEnabled"
    private let feedback = UIImpactFeedbackGenerator(style: .light)

    override init() {
        super.init()
        UserDefaults.standard.register(defaults: [Self.enabledKey: true])
    }

    func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.frameInfo.isMainFrame, BundledWebsite.contains(message.frameInfo.request.url),
              let event = message.body as? [String: String], event["type"] == "combination",
              UserDefaults.standard.bool(forKey: Self.enabledKey) else { return }
        feedback.impactOccurred()
    }
}

final class GameWebView: WKWebView, WKNavigationDelegate, WKUIDelegate {
    private let openExternal: (URL) -> Void

    init(dataStore: WKWebsiteDataStore = .default(),
         openExternal: @escaping (URL) -> Void = { UIApplication.shared.open($0) }) {
        self.openExternal = openExternal
        let configuration = WKWebViewConfiguration()
        configuration.websiteDataStore = dataStore
        configuration.setURLSchemeHandler(BundledWebsite(), forURLScheme: "msw")
        configuration.userContentController.add(CombinationHaptics(), name: "makeSomethingHaptics")
        super.init(frame: .zero, configuration: configuration)
        navigationDelegate = self
        uiDelegate = self
        scrollView.contentInsetAdjustmentBehavior = .never
        scrollView.bounces = false
        if #available(iOS 26.0, *) {
            scrollView.topEdgeEffect.isHidden = true
            scrollView.bottomEdgeEffect.isHidden = true
        }
        #if DEBUG
        isInspectable = true
        #endif
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) { fatalError() }

    func openCatalogue() {
        load(URLRequest(url: BundledWebsite.catalogue))
    }

    func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
        if url == nil { openCatalogue() } else { reload() }
    }

    func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction,
                 decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        if let url = action.request.url, BundledWebsite.contains(url),
           action.targetFrame?.isMainFrame == true,
           ["/index.html", "/make-something.html"].contains(url.path) {
            decisionHandler(.allow)
        } else {
            openExternalLink(action)
            decisionHandler(.cancel)
        }
    }

    func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration,
                 for action: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        openExternalLink(action)
        return nil
    }

    private func openExternalLink(_ action: WKNavigationAction) {
        guard action.navigationType == .linkActivated, action.sourceFrame.isMainFrame,
              BundledWebsite.contains(action.sourceFrame.request.url),
              let url = action.request.url, ["https", "http"].contains(url.scheme) else { return }
        openExternal(url)
    }
}
