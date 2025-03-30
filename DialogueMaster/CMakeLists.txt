project(
    DialogueMaster
    VERSION 0.1
    DESCRIPTION "A dialogue system for games"
)

CPMAddPackage(
    NAME llama.cpp
    GIT_TAG b4997
    GITHUB_REPOSITORY ggml-org/llama.cpp
    OPTIONS "LLAMA_BUILD_COMMON ON"
    )

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME}
    PRIVATE
    src/DialogueMaster.cpp
    )

target_include_directories(${PROJECT_NAME}
    PRIVATE
    include
    )

target_link_libraries(${PROJECT_NAME} PRIVATE common llama ggml ${CMAKE_THREAD_LIBS_INIT})
