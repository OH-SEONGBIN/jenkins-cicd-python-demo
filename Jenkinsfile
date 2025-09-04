pipeline {
  agent { docker { image 'python:3.11-slim' } }
  options { timestamps(); ansiColor('xterm'); buildDiscarder(logRotator(numToKeepStr: '30')) }

  stages {
    stage('Checkout'){ steps { checkout scm } }

    stage('Setup'){
      steps {
        sh '''
          set -eux
          python -V
          pip install -U pip wheel
          pip install -r requirements.txt -r requirements-dev.txt
          mkdir -p reports metrics
          export PYTHONPATH=src
        '''
      }
    }

    stage('Lint'){
      steps {
        sh '''
          flake8 src tests | tee reports/flake8.txt || true
        '''
      }
    }

    stage('Tests (xdist)'){
      steps {
        sh '''
          export PYTHONPATH=src
          pytest -n auto --junitxml=reports/junit.xml \
                 --cov=src --cov-report=xml:reports/coverage.xml --cov-report=term
        '''
      }
    }

    stage('Metrics'){
      steps {
        sh '''
          python tools/ci_metrics.py --junit reports/junit.xml \
                                     --cov reports/coverage.xml \
                                     --flake reports/flake8.txt \
                                     --out metrics/ci_metrics.csv
        '''
      }
    }
  }

  post {
    always {
      junit 'reports/junit.xml'
      archiveArtifacts artifacts: 'reports/**,metrics/**', fingerprint: true
    }
  }
}
