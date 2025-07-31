pipeline {
  agent any

  environment {
    TARGET_URL = "http://docker-zap-py:5020"
    ZAP_REPORT = "zap_report.html"
    ZAP_IMAGE = "ghcr.io/zaproxy/zaproxy:weekly"
    NETWORK = "zap-net"
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/khilarepriya/docker-zap-py.git'
      }
    }

    stage('Create Docker Network') {
      steps {
        sh 'docker network create $NETWORK || true'
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
          docker run -d --name docker-zap-py --network $NETWORK -p 5020:5020 docker-zap-py

          echo "⏳ Waiting for app to respond on internal port 5020..."
          for i in {1..10}; do
            docker run --rm --network $NETWORK curlimages/curl curl -s http://docker-zap-py:5020 && break
            echo "Waiting ($i)..."
            sleep 5
          done
        '''
      }
    }

    stage('Prepare Workspace for ZAP') {
      steps {
        sh '''
          # Ensure file and directory exist with writable permissions
          mkdir -p $WORKSPACE
          touch $WORKSPACE/gen.conf
          chmod -R 777 $WORKSPACE
        '''
      }
    }

    stage('Run ZAP Baseline Scan') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ghcr-creds', usernameVariable: 'GHCR_USER', passwordVariable: 'GHCR_PAT')]) {
          sh '''
            echo "$GHCR_PAT" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

            docker run --rm --network $NETWORK -v $WORKSPACE:/zap/wrk/:rw \
              $ZAP_IMAGE \
              zap-baseline.py \
              -t $TARGET_URL \
              -g gen.conf \
              -r $ZAP_REPORT
          '''
        }
      }
    }

    stage('Publish ZAP Report') {
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
      sh 'docker network rm $NETWORK || true'
    }
  }
}
