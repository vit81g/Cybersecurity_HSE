# Решение задания по развертыванию Nginx в Docker и Kubernetes

## Описание задания

Развернуть Nginx в контейнеризированной среде (Docker и Kubernetes с использованием Minikube), обеспечить доступ к веб-серверу, настроить сетевую политику и проверить сетевые настройки виртуальной машины, соблюдая требования кибербезопасности и нормативные стандарты (ФЗ-152, ISO 27001, PCI DSS, GDPR).

## Предварительные настройки

### Настройка VirtualBox

1. **Скачайте и установите VirtualBox**:
   - Перейдите на официальный сайт: [virtualbox.org](https://www.virtualbox.org/).
   - Скачайте версию для вашей ОС (актуальная версия на 04 октября 2025 — 7.0.x, проверьте на сайте).
   - Установите, следуя инструкциям мастера.
   - **Источник**: [Документация VirtualBox по установке](https://www.virtualbox.org/manual/ch01.html#intro-installing).

2. **Настройка расширения Extension Pack**:
   - Скачайте Extension Pack с сайта VirtualBox.
   - Установите через меню: File > Preferences > Extensions.
   - Это добавляет поддержку USB, VRDP и шифрования дисков.
   - **Источник**: [Документация VirtualBox по Extension Pack](https://www.virtualbox.org/manual/ch01.html#intro-installing-extensions).

3. **Безопасность**:
   - Включите аппаратную виртуализацию в BIOS (VT-x/AMD-V) для повышения производительности и безопасности.
   - Избегайте использования устаревших версий, чтобы минимизировать уязвимости (например, CVE-2023-21930).

### Настройка VMware Player

1. **Скачайте и установите VMware Player**:
   - Перейдите на официальный сайт: [vmware.com](https://www.vmware.com/products/workstation-player.html).
   - Скачайте бесплатную версию для вашей ОС (актуальная версия на 04 октября 2025 — 17.x, проверьте на сайте).
   - Установите, следуя инструкциям мастера.
   - **Источник**: [Документация VMware по установке Player](https://docs.vmware.com/en/VMware-Workstation-Player/17/workstation-player-17-user-guide/GUID-0B6D8E4B-8B34-4A0D-AF0C-0A2D7A7C1A7D.html).

2. **Настройка сетевых адаптеров**:
   - В настройках ВМ выберите Bridged для внешнего доступа или NAT для изоляции.
   - **Источник**: [Документация VMware по сетевым настройкам](https://docs.vmware.com/en/VMware-Workstation-Player/17/workstation-player-17-user-guide/GUID-5A3C3957-3C4B-4B8C-9166-5A43F6D3B7B8.html).

3. **Безопасность**:
   - Включите TPM и Secure Boot в настройках ВМ для соответствия стандартам (например, ISO 27001).
   - Регулярно обновляйте VMware для защиты от уязвимостей (например, CVE-2023-20867).

## Настройка виртуальной машины (ВМ)

### Установка ОС Ubuntu

1. **Создайте ВМ**:
   - В VirtualBox/VMware: New > Укажите имя, тип ОС — Linux, версия — Ubuntu (64-bit).
   - Выделите ресурсы: 2 ГБ RAM, 2 CPU, 20 ГБ диск (динамический).
   - Прикрепите ISO-образ Ubuntu Server 22.04 LTS или новее: [ubuntu.com/download/server](https://ubuntu.com/download/server).
   - **Источник**: [Документация Ubuntu по установке](https://ubuntu.com/tutorials/install-ubuntu-server).

2. **Установка Ubuntu**:
   - Запустите ВМ и следуйте мастеру установки (минимальная установка).
   - Настройте сеть: Bridged для внешнего доступа (получит IP, например, `192.168.108.130`).
   - Обновите систему:
     ```bash
     sudo apt update
     sudo apt upgrade -y
     ```

### Установка программ и пакетов

1. **Установка Docker**:
   ```bash
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   newgrp docker
   ```
   - **Источник**: [Документация Docker для Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

2. **Установка Minikube**:
   ```bash
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```
   - **Источник**: [Документация Minikube](https://minikube.sigs.k8s.io/docs/start/).

3. **Установка kubectl**:
   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install kubectl /usr/local/bin/kubectl
   ```
   - **Источник**: [Документация kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/).

4. **Дополнительные пакеты**:
   - Установите инструменты для сети и безопасности:
     ```bash
     sudo apt install -y curl wget net-tools ufw
     ```
   - Включите файрвол:
     ```bash
     sudo ufw enable
     sudo ufw allow 22/tcp  # SSH
     sudo ufw allow 8080/tcp  # Nginx в Docker
     sudo ufw allow 8443/tcp  # Minikube API
     ```

## Возможные проблемы и их решения

1. **Ошибка доступа к Docker-демону** (`permission denied while trying to connect to the Docker daemon socket`):
   - **Причина**: Пользователь не входит в группу `docker` или изменения группы не применились.
   - **Решение**:
     ```bash
     sudo usermod -aG docker $USER
     newgrp docker
     ```
     Проверьте права сокета:
     ```bash
     ls -l /var/run/docker.sock
     sudo chown root:docker /var/run/docker.sock
     sudo chmod 660 /var/run/docker.sock
     ```
   - **Источник**: [Документация Docker](https://docs.docker.com/engine/install/linux-postinstall/).

2. **Ошибка `kubectl get nodes` (`EOF`)**:
   - **Причина**: Проблемы с прокси или TLS-соединением к API-серверу Minikube (`https://192.168.49.2:8443`).
   - **Решение**:
     - Добавьте IP Minikube в `NO_PROXY`:
       ```bash
       export NO_PROXY=$NO_PROXY,192.168.49.2
       sudo nano /etc/environment
       ```
       Добавьте: `NO_PROXY=localhost,127.0.0.0/8,::1,192.168.49.2`.
       Примените: `source /etc/environment`.
     - Перезапустите Minikube:
       ```bash
       minikube delete
       rm -rf ~/.minikube
       minikube start --driver=docker
       ```
   - **Источник**: [Документация Minikube по прокси](https://minikube.sigs.k8s.io/docs/handbook/vpn_and_proxy/).

3. **Проблемы с прокси**:
   - **Причина**: Прокси (`http://127.0.0.1:2080/`) мешает соединению.
   - **Решение**: Обновите `NO_PROXY` (см. выше) и перезапустите службы.
   - **Источник**: [Документация Docker по прокси](https://docs.docker.com/network/proxy/).

4. **Проблемы с сетевыми настройками**:
   - **Причина**: Неправильная конфигурация адаптера (NAT/Bridged) или файрвол блокирует ICMP.
   - **Решение**:
     - Настройте Bridged в VirtualBox/VMware.
     - Проверьте IP:
       ```bash
       ip addr show ens33
       ```
     - Разрешите ICMP:
       ```bash
       sudo ufw allow proto icmp
       ```
   - **Источник**: [Документация VMware по сетям](https://docs.vmware.com/en/VMware-Workstation-Player/17/workstation-player-17-user-guide/GUID-5A3C3957-3C4B-4B8C-9166-5A43F6D3B7B8.html).

## Развертывание Nginx

### Шаг 1: Запуск Nginx в Docker

1. Запустите контейнер:
   ```bash
   docker run -it --rm -d -p 8080:80 --name web nginx
   ```

2. Проверка:
   ```bash
   docker ps
   curl http://localhost:8080
   ```
![Пример изображения](screenshots/curl.jpg)
   Или откройте `http://localhost:8080` в браузере.

### Шаг 2: Развертывание Nginx в Kubernetes (Minikube)

1. Запустите Minikube:
   ```bash
   minikube start --driver=docker
   ```

2. Создайте файл `nginx-deployment.yaml`:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:latest
           ports:
           - containerPort: 80
   ```

3. Примените манифест:
   ```bash
   kubectl apply -f nginx-deployment.yaml
   ```

4. Создайте файл `nginx-service.yaml`:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx-service
   spec:
     selector:
       app: nginx
     ports:
       - protocol: TCP
         port: 80
         targetPort: 80
         nodePort: 30080
     type: NodePort
   ```

5. Примените манифест:
   ```bash
   kubectl apply -f nginx-service.yaml
   ```

6. Получите IP Minikube:
   ```bash
   minikube ip
   ```

7. Проверьте доступ:
   Откройте `http://<minikube-ip>:30080` в браузере.

### Шаг 3: Настройка сетевой политики

1. Создайте файл `network-policy.yaml`:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-nginx
   spec:
     podSelector:
       matchLabels:
         app: nginx
     policyTypes:
     - Ingress
     ingress:
     - from:
       - ipBlock:
           cidr: 192.168.108.0/24
       ports:
       - protocol: TCP
         port: 80
   ```

2. Примените сетевую политику:
   ```bash
   kubectl apply -f network-policy.yaml
   ```

### Шаг 4: Настройка TLS для Nginx

1. Создайте TLS-секрет:
   ```bash
   kubectl create secret tls nginx-tls --cert=path/to/cert.pem --key=path/to/key.pem
   ```
   - **Источник**: [Документация Kubernetes по TLS](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/).

2. Обновите `nginx-service.yaml` для HTTPS (при необходимости):
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx-service
   spec:
     selector:
       app: nginx
     ports:
       - protocol: TCP
         port: 443
         targetPort: 443
         nodePort: 30443
     type: NodePort
   ```

3. Примените обновление:
   ```bash
   kubectl apply -f nginx-service.yaml
   ```

4. Настройте Nginx для использования TLS (добавьте конфигурацию HTTPS в `nginx-deployment.yaml`, если требуется).

### Шаг 5: Проверка сетевых настроек

1. Определите IP виртуальной машины:
   ```bash
   ip addr show ens33
   ```
   - IP: `192.168.108.130` (интерфейс `ens33`).

2. Проверьте возможность пинга с вашего компьютера:
   ```bash
   ping 192.168.108.130
   ```

3. Разрешите ICMP в файрволе (если пинг не проходит):
   ```bash
   sudo ufw allow proto icmp
   ```

### Шаг 6: Соответствие нормативным требованиям

1. **Шифрование данных в etcd** (ФЗ-152, GDPR):
   - Настройте шифрование:
     ```bash
     kubectl edit -n kube-system configmap kubeadm-config
     ```
   - Следуйте [документации Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/).

2. **Аудит логов** (ISO 27001):
   - Настройте аудит:
     ```bash
     kubectl edit -n kube-system deployment kube-apiserver
     ```
   - Добавьте флаг `--audit-log-path`.

3. **Ограничение привилегий** (PCI DSS):
   - Используйте Pod Security Admission в Kubernetes 1.34.0 для ограничения прав контейнеров.
   - **Источник**: [Документация Kubernetes по безопасности](https://kubernetes.io/docs/concepts/security/overview/).

### Шаг 7: Python-скрипт для диагностики

```python
#!/usr/bin/env python3
import subprocess

def check_docker():
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    print("Контейнеры Docker:", result.stdout.strip())

def check_nginx():
    result = subprocess.run(["curl", "-s", "http://localhost:8080"], capture_output=True, text=True)
    print("Ответ Nginx:", result.stdout[:100] + "..." if result.stdout else "Нет ответа")

def check_minikube():
    result = subprocess.run(["minikube", "status"], capture_output=True, text=True)
    print("Статус Minikube:", result.stdout.strip())

def check_kubectl():
    result = subprocess.run(["kubectl", "get", "nodes"], capture_output=True, text=True)
    print("kubectl get nodes:", result.stdout.strip())

def check_network():
    result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
    print("Сетевые интерфейсы:", result.stdout.strip())
    result = subprocess.run(["ping", "-c", "4", "192.168.108.130"], capture_output=True, text=True)
    print("Пинг 192.168.108.130:", result.stdout.strip())

if __name__ == "__main__":
    print("Проверка Docker...")
    check_docker()
    print("\nПроверка Nginx...")
    check_nginx()
    print("\nПроверка Minikube...")
    check_minikube()
    print("\nПроверка kubectl...")
    check_kubectl()
    print("\nПроверка сети...")
    check_network()
```

Сохраните как `check_setup.py`, сделайте исполняемым и запустите:
```bash
chmod +x check_setup.py
./check_setup.py
```

## Заключение

- Nginx успешно развернут в Docker и Kubernetes.
- Настроены виртуальная машина, безопасность, сетевая политика и TLS.
- IP виртуальной машины: `192.168.108.130`. Пинг возможен при правильной сетевой конфигурации.
- Устранены проблемы с доступом к Docker и соединением с Minikube.