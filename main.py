from server.server import HTTPServer
import handlers
import config

if __name__ == "__main__":
    server = HTTPServer(host=config.HOST, port=config.PORT)
    server.router.add_route("/", handlers.HomeHandler)
    server.router.add_route("/about", handlers.AboutHandler)
    server.router.add_route("/auth", handlers.AuthHandler)
    server.router.add_route("/auth/login", handlers.AuthHandler)
    server.router.add_route("/auth/logout", handlers.AuthHandler)
    server.router.add_route("/profile", handlers.ProfileHandler)
    server.router.establish_default_handler(handlers.DefaultHandler)
    server.run()


