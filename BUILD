load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "shudong_app",
    srcs = [
        "main.py",
        "routes.py",
    ],
    main = "main.py",
    visibility = ["//visibility:public"],
    deps = [
        "//api",
        "@pypi//flask",
    ],
)

exports_files(
    [
        ".ruff.toml",
    ],
    visibility = ["//tools/lint:lint_access_group"],  #lint file group
)

alias(
    name = "format",
    actual = "//tools/format",
)

filegroup(
    name = "all_files",
    srcs = glob(["**/*.py"]),
)

py_test(
    name = "test",
    srcs = ["test.py"],
)
