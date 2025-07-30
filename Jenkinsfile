pipeline {
  agent any

  environment {
    TARGET_URL = "http://localhost:5020"
    ZAP_REPORT = "zap_report.html"
    ZAP_IMAGE = "ghcr.io/zaproxy/zaproxy:weekly"
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/khilarepriya/docker-zap-py.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t docker-zap-py .'
      }
    }

    stage('Start App') {
      steps {
        sh '''
          docker rm -f docker-zap-py || true
          docker run -d --name docker-zap-py -p 5020:5000 docker-zap-py
          sleep 10
        '''
      }
    }

    stage('Run ZAP Baseline Scan') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ghcr-creds', usernameVariable: 'GHCR_USER', passwordVariable: 'GHCR_PAT')]) {
          sh '''
            echo "$GHCR_PAT" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

            docker run --rm -v $WORKSPACE:/zap/wrk/:rw \
              $ZAP_IMAGE \
              zap-baseline.py \
              -t $TARGET_URL \
              -g gen.conf \
              -r $ZAP_REPORT
          '''
        }
      }
    }

    stage('Publish Report') {
      steps {
        publishHTML([
          allowMissing: false,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: '.',
          reportFiles: "${ZAP_REPORT}",
          reportName: 'ZAP Scan Report'
        ])
      }
    }

    stage('Stop App') {
      steps {
        sh '''
          docker stop docker-zap-py || true
          docker rm docker-zap-py || true
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: "${ZAP_REPORT}", fingerprint: true
    }
  }
}

