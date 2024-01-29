import setuptools

setuptools.setup(
    name="venus-trjconv",
    version="0.1.0",
    author="mizu-bai",
    author_email="shiragawa4519@outlook.com",
    description="A VENUS96 trajectory converter",
    url="https://github.com/mizu-bai/venus-trjconv",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.8",
    install_requires=[
        "numpy>1.20.0",
    ],
)
