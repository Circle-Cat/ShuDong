load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")


py_binary(
    name = "shudong_app",
    srcs = ["main.py", "routes.py"],
    main = "main.py",
    deps = [
        "//api:api",
        "@pypi//flask",
    ],
    visibility = ["//visibility:public"],
)

