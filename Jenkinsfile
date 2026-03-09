pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG_PYTHON', defaultValue: '', description: 'Tag de la imagen Docker de python')
        string(name: 'IMAGE_TAG_WAF', defaultValue: '', description: 'Tag de la imagen Docker de waf')
    }

    environment {
        GITHUB_CREDENTIALS = credentials('GitHub')
        KUBERNETES_CREDENTIALS = credentials('Kubernetes')
        DOCKERHUB_CREDENTIALS = credentials('DockerHub')
        SNYK_TOKEN = credentials('snyk-token')
        DOCKER_IMAGE_PYTHON = "grupob3/pepspython"
        DOCKER_IMAGE_WAF = "grupob3/pepsapachewaf"
        FINAL_IMAGE_TAG_PYTHON = "${params.IMAGE_TAG_PYTHON}"
        FINAL_IMAGE_TAG_WAF = "${params.IMAGE_TAG_WAF}"
        KUBERNETES_HOST = "10.227.87.80"
        PYTHON_IMAGE = 'python:3.11-slim'
        TEST_DIR = 'miPrimeraWeb/tests'
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {

        stage('Prueba unitaria') {
            agent {
                docker {
                    image "${PYTHON_IMAGE}"
                    reuseNode true
                }
            }
            steps {
                sh """
                    pip install --no-cache-dir pytest pytest-cov
                    export PYTHONPATH="\${WORKSPACE}/miPrimeraWeb:\${PYTHONPATH}"
                    cd "\${WORKSPACE}/miPrimeraWeb"
                    pytest tests --cov=api/web --cov-fail-under=1 --junitxml=pytest_results.xml
                """
                junit 'miPrimeraWeb/pytest_results.xml'
            }
        }

        stage('Pruebas IaC') {
            steps {
                script {
                    sh '''
                        echo "=== Iniciando escaneo de IaC con Checkov ==="

                        docker run --rm \
                            -v "$(pwd)/miPrimeraWeb":/root/src \
                            bridgecrew/checkov:latest \
                            -d /root/src/api \
                            -d /root/src/apache \
                            --framework dockerfile,kubernetes,helm \
                            -o cli \
                            --soft-fail > checkov-output.txt 2>&1 || true

                        echo ""
                        echo "=== Resumen de Checkov ==="
                        tail -30 checkov-output.txt
                    '''
                }
            }
            post {
                always {
                    sh '''
                        cat > iac-scan-report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Infrastructure as Code Scan Report</title>
</head>
<body>
<h1>IaC Scan Report</h1>
<pre>
EOF
                    cat checkov-output.txt >> iac-scan-report.html
                    cat >> iac-scan-report.html << 'EOF'
</pre>
</body>
</html>
EOF
                    '''

                    archiveArtifacts artifacts: 'checkov-output.txt,iac-scan-report.html'

                    publishHTML([
                        reportDir: '.',
                        reportFiles: 'iac-scan-report.html',
                        reportName: 'IaC Scan Report',
                        allowMissing: true,
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    ])
                }
            }
        }

        stage('Static Analysis') {
            parallel {

                stage('Detect Secrets') {
                    steps {
                        script {
                            catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                sh '''
                                    detect-secrets scan . > detect-secrets.json
                                '''
                            }
                        }
                        archiveArtifacts artifacts: 'detect-secrets.json', allowEmptyArchive: true
                    }
                }

                stage('SonarQube') {
                    steps {
                        script {
                            withSonarQubeEnv('SonarQube') {
                                sh "${SCANNER_HOME}/bin/sonar-scanner"
                            }
                        }
                    }
                }
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DockerHub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Build Docker python') {
            steps {
                script {
                    dockerImagePython = docker.build("${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}", "miPrimeraWeb/api")
                }
            }
        }

        stage('Push Docker python') {
            steps {
                script {
                    dockerImagePython.push(FINAL_IMAGE_TAG_PYTHON)
                }
            }
        }

        stage('Scan Docker Image Python for Vulnerabilities') {
            steps {
                script {
                    sh '''
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --exit-code 0 \
                            --format json \
                            --output trivy-python-report.json \
                            ${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}
                    '''
                }
            }
            post {
                always {
                    sh '''
                        cat > trivy-python-report.html << 'EOF'
<!DOCTYPE html>
<html>
<body>
<h1>Trivy Python Report</h1>
<pre>
EOF
                    cat trivy-python-report.json >> trivy-python-report.html
                    cat >> trivy-python-report.html << 'EOF'
</pre>
</body>
</html>
EOF
                    '''

                    archiveArtifacts artifacts: 'trivy-python-report.json,trivy-python-report.html'

                    publishHTML([
                        reportDir: '.',
                        reportFiles: 'trivy-python-report.html',
                        reportName: 'Trivy Python Scan',
                        allowMissing: true,
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    ])
                }
            }
        }

        stage('Build Docker WAF') {
            when { expression { params.IMAGE_TAG_WAF?.trim() } }
            steps {
                script {
                    dockerImageWaf = docker.build("${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}", "miPrimeraWeb/apache")
                }
            }
        }

        stage('Push Docker waf') {
            when { expression { params.IMAGE_TAG_WAF?.trim() } }
            steps {
                script {
                    dockerImageWaf.push(FINAL_IMAGE_TAG_WAF)
                }
            }
        }

        stage('Scan Docker Image WAF for Vulnerabilities') {
            when { expression { params.IMAGE_TAG_WAF?.trim() } }
            steps {
                script {
                    sh '''
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --exit-code 0 \
                            --format json \
                            --output trivy-waf-report.json \
                            ${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}
                    '''
                }
            }
            post {
                always {
                    sh '''
                        cat > trivy-waf-report.html << 'EOF'
<!DOCTYPE html>
<html>
<body>
<h1>Trivy WAF Report</h1>
<pre>
EOF
                    cat trivy-waf-report.json >> trivy-waf-report.html
                    cat >> trivy-waf-report.html << 'EOF'
</pre>
</body>
</html>
EOF
                    '''

                    archiveArtifacts artifacts: 'trivy-waf-report.json,trivy-waf-report.html'

                    publishHTML([
                        reportDir: '.',
                        reportFiles: 'trivy-waf-report.html',
                        reportName: 'Trivy WAF Scan',
                        allowMissing: true,
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    ])
                }
            }
        }

        stage('Run Application with Docker Compose') {
            steps {
                script {
                    sh '''
                        cat << 'EOF' > .env
                        MARIADB_ROOT_PASSWORD=example
                        MARIADB_USER=agente
                        MARIADB_USER_PASSWORD=0traClave
                        MARIADB_DATABASE=ciber
                        DB_USERNAME=root
                        DB_PASSWORD=example
                        DB_DATABASE=ciber
                        EOF
                    '''
                    sh '''
                        docker compose -f miPrimeraWeb/docker-compose.yml up -d
                    '''
                }
            }
        }

        stage('Vulnerability Scan') {
            steps {
                script {
                    sh 'echo aqui van las pruebas DAST'
                }
            }
        }

        stage('Deploy en Kubernetes') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Kubernetes',
                                                  usernameVariable: 'JUMP_USER',
                                                  passwordVariable: 'JUMP_PASS')]) {
                    sh """
                        sshpass -p '$JUMP_PASS' ssh -o StrictHostKeyChecking=no $JUMP_USER@$KUBERNETES_HOST \\
                          "kubectl set image deployment/python \
                            python=${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON} \
                            -n grupob3 && \\
                          kubectl rollout status deployment/python -n grupob3"
                    """

                    script {
                        if (params.IMAGE_TAG_WAF?.trim()) {
                            sh """
                                sshpass -p '$JUMP_PASS' ssh -o StrictHostKeyChecking=no $JUMP_USER@$KUBERNETES_HOST \\
                                  "kubectl set image deployment/apache-waf \
                                    apache=${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF} \
                                    -n grupob3 && \\
                                  kubectl rollout status deployment/apache-waf -n grupob3"
                            """
                        } else {
                            echo "WAF TAG vacío → No se despliega WAF"
                        }
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    sh 'docker compose -f miPrimeraWeb/docker-compose.yml down -v'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline correcto!'
        }
        failure {
            echo 'Pipeline fallo!'
        }
    }
}
