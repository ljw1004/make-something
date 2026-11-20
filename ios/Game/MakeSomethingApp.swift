import SwiftUI

@main
struct MakeSomethingApp: App {
    var body: some Scene {
        WindowGroup {
            GameView()
                .background(Color(uiColor: .systemBackground))
        }
    }
}

private struct GameView: UIViewRepresentable {
    func makeUIView(context: Context) -> GameWebView {
        let view = GameWebView()
        view.openCatalogue()
        return view
    }

    func updateUIView(_ view: GameWebView, context: Context) {}
}
