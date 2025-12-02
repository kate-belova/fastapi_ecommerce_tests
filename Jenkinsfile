pipeline {
	agent any

	environment {
		USER = ''
		PASSWORD = ''
		DB_NAME = ''
		HOST = ''
		PORT = ''
		SECRET_KEY = ''
	}

	stages {
		stage('Checkout') {
			steps {
				checkout scm
			}
		}

		stage('Setup Python Environment') {
			steps {
				sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
			}
		}

		stage('Create .env and Export secrets') {
			steps {
				withCredentials([
					string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY'),
					string(credentialsId: 'USER', variable: 'USER'),
					string(credentialsId: 'PASSWORD', variable: 'PASSWORD'),
					string(credentialsId: 'DB_NAME', variable: 'DB_NAME'),
					string(credentialsId: 'HOST', variable: 'HOST'),
					string(credentialsId: 'PORT', variable: 'PORT')
				]) {
					sh '''
                        echo "USER=$USER" > .env
                        echo "PASSWORD=$PASSWORD" >> .env
                        echo "DB_NAME=$DB_NAME" >> .env
                        echo "HOST=$HOST" >> .env
                        echo "PORT=$PORT" >> .env
                        echo "SECRET_KEY=$SECRET_KEY" >> .env
                    '''
				}
			}
		}

		stage('Run Tests') {
			steps {
				sh '''
                    . venv/bin/activate
                    pytest
                '''
			}
		}
	}

	post {
		always {
			allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
		}

		success {
			echo '✅ All tests passed successfully!'
		}

		failure {
			echo '❌ Tests failed!'
		}
	}
}