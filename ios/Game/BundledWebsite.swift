import Foundation
import UniformTypeIdentifiers
import WebKit

/// Serves the same directory layout as the published site under a stable save origin.
final class BundledWebsite: NSObject, WKURLSchemeHandler {
    static let catalogue = URL(string: "msw://app/index.html")!
    private let root = Bundle.main.resourceURL!.appendingPathComponent("Website").resolvingSymlinksInPath()

    static func contains(_ url: URL?) -> Bool {
        guard let url else { return false }
        return url.scheme == "msw" && url.host == "app" && url.port == nil && url.user == nil && url.password == nil
    }

    func webView(_ webView: WKWebView, start task: WKURLSchemeTask) {
        guard let url = task.request.url, Self.contains(url),
              let components = URLComponents(url: url, resolvingAgainstBaseURL: false),
              !components.path.contains("\0") else {
            task.didFailWithError(URLError(.badURL))
            return
        }
        let file = root.appendingPathComponent(components.path).standardizedFileURL.resolvingSymlinksInPath()
        guard file.path.hasPrefix(root.path + "/") else {
            task.didFailWithError(URLError(.noPermissionsToReadFile))
            return
        }
        do {
            let data = try Data(contentsOf: file, options: .mappedIfSafe)
            let mime: String
            switch file.pathExtension.lowercased() {
            case "js": mime = "text/javascript"
            case "md": mime = "text/markdown"
            default: mime = UTType(filenameExtension: file.pathExtension)?.preferredMIMEType ?? "application/octet-stream"
            }
            let headers = [
                "Content-Type": mime,
                "Content-Security-Policy": "default-src msw://app; script-src msw://app 'unsafe-inline'; worker-src blob:; style-src msw://app 'unsafe-inline'; img-src msw://app data:; manifest-src data:; object-src 'none'; frame-src 'none'; base-uri 'none'"
            ]
            task.didReceive(HTTPURLResponse(url: url, statusCode: 200, httpVersion: nil, headerFields: headers)!)
            task.didReceive(data)
            task.didFinish()
        } catch {
            task.didFailWithError(error)
        }
    }

    // Requests finish synchronously on WebKit's callback queue.
    func webView(_ webView: WKWebView, stop task: WKURLSchemeTask) {}
}
