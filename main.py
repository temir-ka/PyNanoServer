from server.server import HTTPServer
import handlers
import config

app = HTTPServer()

if __name__ == "__main__":
    #app = HTTPServer()
    app.load_config_from_pyfile("config.py")
    app.router.add_route("/", handlers.home)
    # server.router.add_route("/about", handlers.AboutHandler)
    # server.router.add_route("/auth", handlers.AuthHandler)
    # server.router.add_route("/auth/login", handlers.AuthHandler)
    # server.router.add_route("/auth/logout", handlers.AuthHandler)
    # server.router.add_route("/profile", handlers.ProfileHandler)
    # server.router.establish_default_handler(handlers.DefaultHandler)
    app.create_socket()
    app.run()


