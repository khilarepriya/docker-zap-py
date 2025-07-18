pipeline {
  agent any

  environment {
    TARGET_URL = "http://localhost:5020"
    ZAP_REPORT = "zap_report.html"
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
        sh 'docker run -d --name docker-zap-py -p 5000:5000 docker-zap-py'
        sleep 10 // wait for app to start
      }
    }

    stage('Run ZAP Baseline Scan') {
      steps {
        sh '''
          docker run --rm -v $PWD:/zap/wrk/:rw \
            owasp/zap2docker-stable zap-baseline.py \
            -t $TARGET_URL \
            -g gen.conf \
            -r $ZAP_REPORT || true
        '''
      }
    }

    stage('Publish Report') {
      steps {
        publishHTML([
          allowMissing: false,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: '.',
          reportFiles: 'zap_report.html',
          reportName: 'ZAP Scan Report'
        ])
      }
    }

    stage('Stop App') {
      steps {
        sh 'docker stop docker-zap-py && docker rm docker-zap-py'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'zap_report.html', fingerprint: true
    }
  }
}
