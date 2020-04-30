node('linux') {
    container('buildkit') {
        def rev

        stage('checkout scm') {
            rev = checkout(scm)
        }

        # run linter on the codebase

        # sonarqube?

        stage('Build docker-image') {
            # docker build that pulls down and includes dependencies
            dockerBuild()
        }

        # run tests within the built docker image

        stage('Publish image') {
            withCredentials([usernamePassword(credentialsId: "dockerhub-digiratidlcs", usernameVariable: 'registryUsername', passwordVariable: 'registryPassword')]) {
                dockerPush(registryUsername, registryPassword, rev.GIT_COMMIT)
            }
        }
    }
}

def dockerBuild() {
    steps {
        sh "docker build -t digirati/appetiser:latest ."
    }
}

def dockerPush(def registryUsername, def registryPassword, def buildNumber) {
    steps {
        sh "docker login --username \"${registryUsername}\" --password \"${registryPassword}\""
        sh "docker tag digirati/appetiser:latest digirati/appetiser:${buildNumber}"
        sh "docker push digirati/appetiser:${buildNumber}"
    }
}
