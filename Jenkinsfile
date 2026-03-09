pipeline {
    agent any

    tools {
        dockerTool "Docker"
    }

    parameters {
        string(
            name: 'IMAGE_TAG_PYTHON',
            defaultValue: '',
            description: 'Tag de la imagen Docker de python'
        )
        string(
            name: 'IMAGE_TAG_WAF',
            defaultValue: '',
            description: 'Tag de la imagen Docker de waf'
        )
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
        stage('Clonar repositorio') {
            steps {
                git url: 'https://github.com/chincheto77-peps/Primera-Fase.git', 
                    branch: 'main',
                    credentialsId: 'GitHub'
            }
        }

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
                    // Ejecutar Checkov y guardar salida
                    sh '''
                        echo "=== Iniciando escaneo de IaC con Checkov ==="
                        
                        # Ejecutar Checkov en contenedor
                        docker run --rm \
                            -v "$(pwd)/miPrimeraWeb":/root/src \
                            bridgecrew/checkov:latest \
                            -d /root/src/api \
                            -d /root/src/apache \
                            --framework dockerfile,kubernetes,helm \
                            -o cli \
                            --soft-fail > checkov-output.txt 2>&1 || true
                        
                        # Mostrar resumen
                        echo ""
                        echo "=== Resumen de Checkov ==="
                        tail -30 checkov-output.txt
                    '''
                }
            }
            post {
                always {
                    // Crear reporte HTML para visualización
                    sh '''
                        cat > iac-scan-report.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>Infrastructure as Code Scan Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        .section { margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007bff; }
        .success { border-left-color: #28a745; }
        .info { border-left-color: #17a2b8; }
        pre { background-color: #f4f4f4; padding: 10px; overflow-x: auto; font-size: 12px; max-height: 400px; }
        code { font-family: 'Courier New', monospace; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Infrastructure as Code Security Scan Report</h1>
        
        <div class="section success">
            <h2>✓ Scan Status</h2>
            <p><strong>Status:</strong> COMPLETED</p>
            <p class="timestamp"><strong>Timestamp:</strong> HTMLEOF
                        date -Iseconds >> iac-scan-report.html
                        cat >> iac-scan-report.html << 'HTMLEOF'
</p>
        </div>
        
        <div class="section info">
            <h2>📁 Directories Scanned</h2>
            <ul>
                <li><code>miPrimeraWeb/api</code></li>
                <li><code>miPrimeraWeb/apache</code></li>
            </ul>
        </div>
        
        <div class="section info">
            <h2>🛠️ Frameworks Analyzed</h2>
            <ul>
                <li>Dockerfile</li>
                <li>Kubernetes</li>
                <li>Helm Charts</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📊 Scan Output</h2>
            <pre><code>
HTMLEOF
                        cat checkov-output.txt >> iac-scan-report.html
                        cat >> iac-scan-report.html << 'HTMLEOF'
            </code></pre>
        </div>
        
        <div class="section success">
            <h2>✓ Report Generated</h2>
            <p>Checkov infrastructure as code security scan completed successfully.</p>
        </div>
    </div>
</body>
</html>
HTMLEOF
                        echo "✓ HTML Report generated: iac-scan-report.html"
                    '''
                    
                    // Archivar los archivos
                    archiveArtifacts artifacts: 'checkov-output.txt,iac-scan-report.html', 
                                     allowEmptyArchive: true
                    
                    // Publicar el HTML como un reporte
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

        stage('Build Docker python'){
            steps{
                script{
                    dockerImagePython= docker.build("${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}", "miPrimeraWeb/api")
                }
            }
        }

        stage('Push Docker python'){
            steps{
                script{
                    dockerImagePython.push(FINAL_IMAGE_TAG_PYTHON)
                } 
            }
        }

        stage('Scan Docker Image Python for Vulnerabilities') {
            steps {
                script {
                    sh '''
                        echo "=== Iniciando escaneo de vulnerabilidades con Trivy ==="
                        echo "Imagen: ${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}"
                        echo ""
                        
                        # Ejecutar Trivy contra la imagen Docker
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --exit-code 0 \
                            --format json \
                            --output trivy-python-report.json \
                            ${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}
                        
                        # Mostrar resumen en tabla
                        echo ""
                        echo "=== Resumen del Escaneo ==="
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --exit-code 0 \
                            ${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}
                    '''
                }
            }
            post {
                always {
                    // Crear reporte HTML
                    sh '''
                        cat > trivy-python-report.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>Trivy Vulnerability Scan - Python Image</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #d9534f; border-bottom: 3px solid #d9534f; padding-bottom: 10px; }
        .section { margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007bff; }
        .critical { border-left-color: #d9534f; background-color: #f8d7da; }
        .high { border-left-color: #ff9800; }
        pre { background-color: #f4f4f4; padding: 10px; overflow-x: auto; font-size: 12px; max-height: 500px; }
        code { font-family: 'Courier New', monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Trivy Container Vulnerability Scan Report - Python Image</h1>
        
        <div class="section">
            <h2>📦 Image Information</h2>
            <p><strong>Image:</strong> <code>${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON}</code></p>
            <p><strong>Scanner:</strong> Trivy</p>
            <p><strong>Severity Filter:</strong> HIGH, CRITICAL</p>
            <p><strong>Scan Date:</strong> <code>$(date -Iseconds)</code></p>
        </div>
        
        <div class="section critical">
            <h2>⚠️ Scan Results</h2>
            <pre><code>
HTMLEOF
                        if [ -f trivy-python-report.json ]; then
                            echo "Report JSON found" >> trivy-python-report.html
                            cat trivy-python-report.json >> trivy-python-report.html
                        else
                            echo "Scan completed. Check detailed results in console output." >> trivy-python-report.html
                        fi
                        cat >> trivy-python-report.html << 'HTMLEOF'
            </code></pre>
        </div>
        
        <div class="section">
            <h2>✓ Scan Information</h2>
            <p>For detailed vulnerability information, check the JSON report in artifacts or console logs.</p>
        </div>
    </div>
</body>
</html>
HTMLEOF
                    '''
                    
                    // Archivar reportes
                    archiveArtifacts artifacts: 'trivy-python-report.json,trivy-python-report.html', 
                                     allowEmptyArchive: true
                    
                    // Publicar HTML
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

        stage('Build Docker WAF'){
            when {
                expression { params.IMAGE_TAG_WAF?.trim() }
            } 
            steps{
                script{
                    dockerImageWaf= docker.build("${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}", "miPrimeraWeb/apache")
                }
            }
        }

        stage('Push Docker waf'){
            when {
                expression { params.IMAGE_TAG_WAF?.trim() }
            }
            steps{
                script{
                    dockerImageWaf.push(FINAL_IMAGE_TAG_WAF)
                }
            }
        }

        stage('Scan Docker Image WAF for Vulnerabilities') {
            when {
                expression { params.IMAGE_TAG_WAF?.trim() }
            }
            steps {
                script {
                    sh '''
                        echo "=== Iniciando escaneo de vulnerabilidades con Trivy ==="
                        echo "Imagen: ${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}"
                        echo ""
                        
                        # Ejecutar Trivy contra la imagen Docker
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --exit-code 0 \
                            --format json \
                            --output trivy-waf-report.json \
                            ${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}
                        
                        # Mostrar resumen en tabla
                        echo ""
                        echo "=== Resumen del Escaneo ==="
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --exit-code 0 \
                            ${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}
                    '''
                }
            }
            post {
                always {
                    // Crear reporte HTML
                    sh '''
                        cat > trivy-waf-report.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>Trivy Vulnerability Scan - WAF Image</title>
    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #d9534f; border-bottom: 3px solid #d9534f; padding-bottom: 10px; }
        .section { margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007bff; }
        .critical { border-left-color: #d9534f; background-color: #f8d7da; }
        .high { border-left-color: #ff9800; }
        pre { background-color: #f4f4f4; padding: 10px; overflow-x: auto; font-size: 12px; max-height: 500px; }
        code { font-family: 'Courier New', monospace; }
                    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Trivy Container Vulnerability Scan Report - WAF Image</h1>
        
        <div class="section">
            <h2>📦 Image Information</h2>
            <p><strong>Image:</strong> <code>${DOCKER_IMAGE_WAF}:${FINAL_IMAGE_TAG_WAF}</code></p>
            <p><strong>Scanner:</strong> Trivy</p>
            <p><strong>Severity Filter:</strong> HIGH, CRITICAL</p>
            <p><strong>Scan Date:</strong> <code>$(date -Iseconds)</code></p>
        </div>
        
        <div class="section critical">
            <h2>⚠️ Scan Results</h2>
            <pre><code>
HTMLEOF
                        if [ -f trivy-waf-report.json ]; then
                            echo "Report JSON found" >> trivy-waf-report.html
                            cat trivy-waf-report.json >> trivy-waf-report.html
                        else
                            echo "Scan completed. Check detailed results in console output." >> trivy-waf-report.html
                        fi
                        cat >> trivy-waf-report.html << 'HTMLEOF'
            </code></pre>
        </div>
        
        <div class="section">
            <h2>✓ Scan Information</h2>
            <p>For detailed vulnerability information, check the JSON report in artifacts or console logs.</p>
        </div>
    </div>
</body>
</html>
HTMLEOF
                    '''
                    
                    // Archivar reportes
                    archiveArtifacts artifacts: 'trivy-waf-report.json,trivy-waf-report.html', 
                                     allowEmptyArchive: true
                    
                    // Publicar HTML
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
            script {
                if (env.WORKSPACE) {
                    cleanWs()
                } else {
                    echo 'No hay workspace, se omite cleanWs'
                }
            }
        }

        success {
            echo 'Pipeline correcto!'
        }

        failure {
            echo 'Pipeline fallo!'
        }
    }
}
