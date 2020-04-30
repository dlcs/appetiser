node('linux') {
    container('buildkit') {
        def rev

        stage('checkout scm') {
            rev = checkout(scm)
        }

        stage('Build docker-image') {
            dockerBuild()
        }

        stage('Publish image') {
            withCredentials([usernamePassword(credentialsId: "dockerhub-digiratidlcs", usernameVariable: 'registryUsername', passwordVariable: 'registryPassword')]) {
                dockerPush(registryUsername, registryPassword, rev.GIT_COMMIT)
            }
        }
    }
}

def runPreCommit() {
    steps {
        sh "pre-commit run --all-files"
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
