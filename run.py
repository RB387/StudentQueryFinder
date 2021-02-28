from simio_di import DependencyInjector, SingletoneDependenciesContainer

from config import get_config

from cli import MainActivity


def main():
    config = get_config()

    injector = DependencyInjector(config, SingletoneDependenciesContainer())
    cli = injector.inject(MainActivity)()  # внедрили зависимости и инициализировали класс

    cli.start()


if __name__ == "__main__":
    main()
