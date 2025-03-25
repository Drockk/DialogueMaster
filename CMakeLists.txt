cmake_minimum_required(VERSION 3.20)

project(
    DialogueMaster
    VERSION 0.1
    DESCRIPTION "A dialogue system for games"
    LANGUAGES CXX
)

find_package(llama-cpp REQUIRED)

add_executable(DialogueMaster)

target_sources(DialogueMaster
    PRIVATE
        src/main.cpp
)

install(TARGETS DialogueMaster RUNTIME)

file(GLOB MODEL_FILES "${CMAKE_SOURCE_DIR}/models/*")
install(FILES ${MODEL_FILES} DESTINATION models)

target_link_libraries(DialogueMaster PRIVATE llama-cpp::llama-cpp ${CMAKE_THREAD_LIBS_INIT})
