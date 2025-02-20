load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "api",
    srcs = ["event_handler.py", "messages.py"],
    deps = [
        "@pypi//flask",
        "//static:static_constants",
    ],
    visibility = ["//visibility:public"],
)