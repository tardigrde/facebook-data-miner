from setuptools import setup


def setup_package() -> None:
    setup(
        name="facebook-data-miner",
        version="0.1.0",
        author="Levente Csőke",
        author_email="leventec3@gmail.com",
        url="https://github.com/tardigrde/facebook-data-miner",
        description="An object-oriented approach "
        "to mining personal Facebook data.",
        license="GPL-3.0",
        keywords="facebook-data,facebook-data-miner,facebook-data-analyzer",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Development Status :: 3 - Alpha",
        ],
        packages=["miner"],
    )


if __name__ == "__main__":
    setup_package()
