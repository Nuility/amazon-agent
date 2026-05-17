"""安装脚本"""
from setuptools import setup, find_packages

setup(
    name="agenttest",
    version="1.0.0",
    description="用户管理智能体系统",
    author="Huawei Cloud CodeArts",
    python_requires=">=3.8",
    packages=find_packages(),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "agenttest=main:main",
        ],
    },
    install_requires=[
        "pyyaml>=5.4",
        "python-dotenv>=0.19",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
