cmake_minimum_required(VERSION 3.20)

include("cmake/get_cpm.cmake")

project(
    DialogueMaster
    VERSION 0.1
    DESCRIPTION "A dialogue system for games"
)

CPMAddPackage(
    NAME llama.cpp
    GIT_TAG b4743
    GITHUB_REPOSITORY ggml-org/llama.cpp
    OPTIONS "LLAMA_BUILD_COMMON ON"
    )

add_subdirectory(DialogueMaster)
