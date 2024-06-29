import subprocess
import os
import sys

def find_all_java_pids():
    try:
        if sys.platform == 'win32':
            jps = 'jps.exe'
        else:
            jps = 'jps'

        # Get the JAVA_HOME environment variable
        java_home = os.environ.get('JAVA_HOME')
        if not java_home:
            raise EnvironmentError("JAVA_HOME environment variable is not set.")

        # Construct the path to the JDK bin directory
        jdk_bin_path = os.path.join(java_home, 'bin')

        # Run the `jps` command from the JDK bin directory
        result = subprocess.run([os.path.join(jdk_bin_path, jps)], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        java_pids = []

        # Iterate through the output lines
        for line in output.splitlines():
            parts = line.split()
            pid = int(parts[0])
            process_name = parts[1] if len(parts) > 1 else ''
            if process_name != 'Jps':
                java_pids.append(pid)

        if java_pids:
            print("Java process PIDs found:")
            for pid in java_pids:
                print(pid)
        else:
            print("No Java process found.")
        
        return java_pids

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    java_pids = find_all_java_pids()
