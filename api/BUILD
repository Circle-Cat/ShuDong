load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "api",
    srcs = [
        "event_handler.py",
        "messages.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//static:static_constants",
        "@pypi//flask",
    ],
)

py_test(
    name = "event_handler_test",
    srcs = ["event_handler_test.py"],
    deps = [
        "//api",
    ],
)
