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
      DOCKER_IMAGE_PYTHON = "grupob3/pepspython"
      DOCKER_IMAGE_WAF = "grupob3/pepsapachewaf"
      FINAL_IMAGE_TAG_PYTHON = "${params.IMAGE_TAG_PYTHON}"
      FINAL_IMAGE_TAG_WAF = "${params.IMAGE_TAG_WAF}"
      KUBERNETES_HOST = "10.227.87.80"
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
        steps {
          sh 'echo aqui se hace la prueba unitaria'
        }
      }

      stage('Static Analysis') {
        parallel {
          stage('Detect Secrets') {
            steps{
                script {
                    // Ejemplo de como capturar el error y dejar que continue el pipeline
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        sh 'echo detect secrets && exit 0' 
                    }
                }
            }
          }
          stage('SonarQube') {
            steps {
              script {
                withSonarQubeEnv('SonarQube') {
                sh "sonar-scanner"
                }
              }
            }
          }

          stage('SCA') {
            steps { 
              sh 'echo sca' 
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
              sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin' //así no apare la clave en el log
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
            // Escanear la imagen Docker usando docker scan
            sh 'echo aqui va el escaneo de imagen python'
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

      stage('Scan Docker Image Waf for Vulnerabilities') {
        when {
          expression { params.IMAGE_TAG_WAF?.trim() }
        }
	      steps {
          script {
            // Escanear la imagen Docker
            sh 'echo aqui escaneo imagen waf'
          }
        }
     }

      stage('Run Application with Docker Compose') {
        steps {
          script {
            // Ejecutar la aplicación con Docker Compose
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
            // Ejecutar escaneo para detectar vulnerabilidades en la aplicación desplegada
            sh 'echo aqui van las pruebas DAST'
          }
        }
      }

stage('Deploy en Kubernetes') {
  steps {
    // Usamos credenciales tipo Username with password de Jenkins
    withCredentials([usernamePassword(credentialsId: 'Kubernetes', 
                                      usernameVariable: 'JUMP_USER', 
                                      passwordVariable: 'JUMP_PASS')]) {
      // Despliegue del servicio Python
      sh """
        sshpass -p '$JUMP_PASS' ssh -o StrictHostKeyChecking=no $JUMP_USER@$KUBERNETES_HOST \\
          "kubectl set image deployment/python \
            python=${DOCKER_IMAGE_PYTHON}:${FINAL_IMAGE_TAG_PYTHON} \
            -n grupob3 && \\

          kubectl rollout status deployment/python -n grupob3"
      """

      // Despliegue del WAF si corresponde
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
            // Detener los contenedores después de la prueba
            sh '''
                docker compose -f miPrimeraWeb/docker-compose.yml down -v
               '''
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
        // Enviar notificación o realizar acciones después de la ejecución exitosa
        echo 'Pipeline correcto!'}

      failure {
        // Enviar notificación en caso de fallo
        echo 'Pipeline fallo!'
      }
    }
}
