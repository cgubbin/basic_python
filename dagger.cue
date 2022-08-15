package base_environment

import (
  "dagger.io/dagger"
  "universe.dagger.io/docker"
)

dagger.#Plan & {
    client: filesystem: ".": read: {
      contents: dagger.#FS
      include: [
      "src", "docs", "conda-linux-64.lock", "poetry.lock", "pyproject.toml", "noxfile.py", "tests",
      ".flake8", ".coverage", ".darglint", ".pyre_configuration", ".watchmanconfig"
      ]
    }

    actions: {
      build: docker.#Build & {
        steps: [
          docker.#Pull & {
              source: "continuumio/miniconda3"
            },

          docker.#Copy & {
              contents: client.filesystem.".".read.contents
              dest: "/app"
            },

          docker.#Run & {
              command: {
                  name: "pip"
                  args: ["install", "conda-lock[pip_support]"]
                }
            },

          docker.#Run & {
              command: {
                  name: "conda-lock"
                  args: ["install", "--conda", "conda", "--name", "app", "/app/conda-linux-64.lock"]

                }
            },

          docker.#Run & {
              command: {
                  name: "pip"
                  args: ["uninstall", "-y", "conda-lock"]
                }
            },

          docker.#Run & {
              workdir: "/app"
              command: {
                  name: "conda"
                  args: ["run", "--no-capture-output", "-n", "app", "poetry", "install"]
                }
            },

          docker.#Set & {
              input: _
              config: env: PATH: "/opt/conda/envs/app/bin:\(input.config.env.PATH)"
            }
        ]
      }

      image: build.output

      lint: {
        docker.#Run & {
          input: image
          workdir: "./app"
          command: {
            name: "nox"
            args: ["-s", "lint"]
            }
          }
      }

      doctest: {
        docker.#Run & {
          input: image
          workdir: "./app"
          command: {
            name: "nox"
            args: ["-s", "xdoctest"]
            }
          }
      }

      typecheck: {
        docker.#Run & {
          input: image
          workdir: "./app"
          command: {
            name: "nox"
            args: ["-s", "pyre"]
            }
          }
      }

      typeguard: {
        docker.#Run & {
          input: image
          workdir: "./app"
          command: {
            name: "nox"
            args: ["-s", "typeguard"]
            }
          }
      }

      test: {
        docker.#Run & {
          input: image
          workdir: "./app"
          command: {
            name: "nox"
            args: ["-s", "tests"]
            }
          }
      }
 }
}
