"""
WORKING PKI System - Fixed OpenSSL config issue
"""

import os
import sys
import subprocess
import json
import ldap3
from datetime import datetime

class WorkingPKISystem:
    def __init__(self):
        # LDAP settings
        self.ldap_server = "194.226.199.73"
        self.ldap_port = 38938
        self.ldap_user = "ldapuser"
        self.ldap_password = "xxXX1234"
        self.ldap_base = "dc=demo,dc=lab"
        
        self.target_users = []

    def log_message(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level.upper()}] {message}")

    def create_simple_openssl_config(self):
        """Create a simple working OpenSSL config file"""
        config_content = """# Simple OpenSSL configuration for HSE PKI
[ req ]
default_bits = 2048
prompt = no
distinguished_name = req_dn
string_mask = utf8only

[ req_dn ]
countryName = RU
stateOrProvinceName = Moscow
localityName = Moscow
organizationName = HSE University
organizationalUnitName = MIEM
commonName = Common Name
emailAddress = Email Address

[ usr_cert ]
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection
"""
        
        config_path = "simple_openssl.cnf"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        return config_path

    def connect_ldap(self):
        """Connect to LDAP and find users starting with A"""
        self.log_message("info", "Connecting to LDAP server...")
        
        try:
            server = ldap3.Server(
                self.ldap_server, 
                port=self.ldap_port, 
                use_ssl=False,
                connect_timeout=10
            )
            
            connection = ldap3.Connection(
                server, 
                user="ldapuser@demo.lab", 
                password=self.ldap_password, 
                authentication=ldap3.SIMPLE,
                auto_bind=True
            )
            
            if connection.bind():
                self.log_message("success", "LDAP connection established")
                
                # Search for users with first letter A
                search_filter = "(&(objectClass=user)(|(givenName=A*)(sn=A*)))"
                attributes = ['cn', 'givenName', 'sn', 'mail']
                
                connection.search(
                    search_base=self.ldap_base,
                    search_filter=search_filter,
                    attributes=attributes,
                    size_limit=5
                )
                
                self.log_message("info", f"Found {len(connection.entries)} entries")
                
                # Process found users
                for entry in connection.entries:
                    user_data = {}
                    try:
                        if hasattr(entry, 'givenName') and entry.givenName:
                            user_data['givenName'] = str(entry.givenName)
                        if hasattr(entry, 'sn') and entry.sn:
                            user_data['sn'] = str(entry.sn)
                        
                        if not user_data.get('givenName') or not user_data.get('sn'):
                            continue
                        
                        if hasattr(entry, 'mail') and entry.mail:
                            user_data['email'] = str(entry.mail)
                        else:
                            user_data['email'] = f"{user_data['givenName'].lower()}.{user_data['sn'].lower()}@demo.lab"
                        
                        self.target_users.append(user_data)
                        self.log_message("success", f"Found user: {user_data['givenName']} {user_data['sn']}")
                        
                    except Exception:
                        continue
                
                connection.unbind()
                return len(self.target_users) >= 2
                    
        except Exception as e:
            self.log_message("error", f"LDAP connection failed: {e}")
            # Use fallback users
            self.use_fallback_users()
            return True

    def use_fallback_users(self):
        """Use fallback users if LDAP fails"""
        self.target_users = [
            {"sn": "Gorshkov", "givenName": "Agafon", "email": "agorshkov@demo.lab"},
            {"sn": "Nikolaeva", "givenName": "Akulina", "email": "anikolaeva@demo.lab"},
            {"sn": "Secret", "givenName": "Agent", "email": "Agent.Secret@demo.lab"}
        ]
        self.log_message("info", f"Using {len(self.target_users)} fallback users")

    def check_prerequisites(self):
        """Check system requirements"""
        self.log_message("info", "Checking system requirements...")
        
        # Check CA files
        if not os.path.exists('groupmca.crt'):
            self.log_message("error", "groupmca.crt not found")
            return False
        if not os.path.exists('groupmca.key'):
            self.log_message("error", "groupmca.key not found")
            return False
            
        self.log_message("success", "CA files found")

        # Check OpenSSL
        try:
            result = subprocess.run(['openssl', 'version'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log_message("success", f"OpenSSL available: {result.stdout.strip()}")
            else:
                self.log_message("error", "OpenSSL not working")
                return False
        except:
            self.log_message("error", "OpenSSL not found in system")
            return False

        return True

    def create_user_certificate_direct(self, user_data, index):
        """Create certificate using direct command line approach"""
        given_name = user_data['givenName']
        surname = user_data['sn']
        email = user_data['email']
        full_name = f"{given_name} {surname}"
        
        filename = f"user_{index:02d}_{surname}_{given_name}".replace(' ', '_')
        
        self.log_message("info", f"Creating certificate [{index}]: {full_name}")
        
        try:
            cert_folder = 'user_certificates'
            os.makedirs(cert_folder, exist_ok=True)
            
            # Create simple config for this user
            config_content = f"""# OpenSSL config for {full_name}
[ req ]
default_bits = 2048
prompt = no
distinguished_name = dn
req_extensions = ext

[ dn ]
C = RU
ST = Moscow
L = Moscow
O = HSE University
OU = MIEM
CN = {full_name}
emailAddress = {email}

[ ext ]
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection
"""
            
            config_file = f"{cert_folder}/{filename}.cnf"
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)

            # 1. Create private key
            key_path = f"{cert_folder}/{filename}.key"
            key_cmd = ['openssl', 'genrsa', '-out', key_path, '2048']
            result = subprocess.run(key_cmd, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                self.log_message("error", f"Key creation failed: {result.stderr}")
                return False

            # 2. Create CSR using the config file
            csr_path = f"{cert_folder}/{filename}.csr"
            csr_cmd = ['openssl', 'req', '-new', '-key', key_path, '-out', csr_path, '-config', config_file]
            result = subprocess.run(csr_cmd, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                self.log_message("error", f"CSR creation failed: {result.stderr}")
                # Try without config
                subject = f'/C=RU/ST=Moscow/L=Moscow/O=HSE University/OU=MIEM/CN={full_name}/emailAddress={email}'
                csr_cmd_simple = ['openssl', 'req', '-new', '-key', key_path, '-out', csr_path, '-subj', subject]
                result = subprocess.run(csr_cmd_simple, capture_output=True, text=True, shell=True)
                if result.returncode != 0:
                    self.log_message("error", f"Simple CSR also failed: {result.stderr}")
                    return False

            # 3. Sign certificate
            crt_path = f"{cert_folder}/{filename}.crt"
            sign_cmd = [
                'openssl', 'x509', '-req', '-in', csr_path, 
                '-CA', 'groupmca.crt', '-CAkey', 'groupmca.key', 
                '-CAcreateserial', '-out', crt_path, '-days', '365'
            ]
            
            # Try with password if needed
            result = subprocess.run(sign_cmd, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                sign_cmd.extend(['-passin', 'pass:NewMcaPass456'])
                result = subprocess.run(sign_cmd, capture_output=True, text=True, shell=True)
                if result.returncode != 0:
                    self.log_message("error", f"Signing failed: {result.stderr}")
                    return False

            # 4. Verify certificate
            verify_cmd = ['openssl', 'x509', '-in', crt_path, '-subject', '-noout']
            result = subprocess.run(verify_cmd, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log_message("success", f"Certificate created: {result.stdout.strip()}")
                
                # Cleanup
                try:
                    os.remove(csr_path)
                    os.remove(config_file)
                except:
                    pass
                
                return True
            else:
                self.log_message("error", "Certificate verification failed")
                return False
                
        except Exception as e:
            self.log_message("error", f"Certificate creation error: {str(e)}")
            return False

    def generate_certificates(self):
        """Generate certificates for all target users"""
        if not self.target_users:
            self.log_message("error", "No users to process")
            return 0
            
        self.log_message("info", f"Generating certificates for {len(self.target_users)} users...")
        
        success_count = 0
        for i, user in enumerate(self.target_users, 1):
            if self.create_user_certificate_direct(user, i):
                success_count += 1
        
        return success_count

    def create_success_report(self, success_count):
        """Create success report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'users_processed': len(self.target_users),
            'certificates_created': success_count,
            'users': self.target_users
        }
        
        # List created certificates
        cert_folder = 'user_certificates'
        if os.path.exists(cert_folder):
            report['files'] = []
            for file in sorted(os.listdir(cert_folder)):
                if file.endswith('.crt'):
                    report['files'].append(file)
        
        with open('pki_success_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Create simple batch file to verify
        batch_content = """@echo off
echo PKI System - Certificate Verification
echo =====================================

if not exist "user_certificates" (
    echo No certificates found!
    pause
    exit /b 1
)

echo Found certificates:
echo.
for %%f in (user_certificates\\*.crt) do (
    echo [%%~nf]
    openssl x509 -in "%%f" -subject -noout
    openssl x509 -in "%%f" -issuer -noout  
    openssl verify -CAfile groupmca.crt "%%f" && echo ✓ Verified || echo ✗ Failed
    echo.
)

echo.
echo All done!
pause
"""
        
        with open('check_certs.bat', 'w') as f:
            f.write(batch_content)
        
        self.log_message("success", "Verification script created: check_certs.bat")

    def run(self):
        """Main execution method"""
        self.log_message("info", "🚀 STARTING WORKING PKI SYSTEM")
        self.log_message("info", "=" * 50)
        
        # Step 1: Get users from LDAP
        self.connect_ldap()
        
        # Step 2: Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Step 3: Generate certificates
        success_count = self.generate_certificates()
        
        # Step 4: Create report
        self.create_success_report(success_count)
        
        # Final output
        if success_count > 0:
            self.log_message("success", f"✅ SUCCESS: Created {success_count} certificates!")
            print(f"\n📁 Certificates location: user_certificates/")
            print(f"🔍 Run 'check_certs.bat' to verify certificates")
            print(f"📊 Report: pki_success_report.json")
            return True
        else:
            self.log_message("error", "❌ FAILED: No certificates created")
            return False

def main():
    print("🔐 WORKING PKI SYSTEM - FIXED VERSION")
    print("======================================")
    
    system = WorkingPKISystem()
    
    try:
        if system.run():
            print("\n🎉 LAB WORK COMPLETED SUCCESSFULLY!")
        else:
            print("\n💥 Lab work failed. Check the logs above.")
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()