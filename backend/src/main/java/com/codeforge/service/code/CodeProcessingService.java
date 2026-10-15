package com.codeforge.service.code;

import com.codeforge.entity.CodeChunk;
import com.codeforge.entity.CodeDocument;
import com.codeforge.entity.Project;
import com.codeforge.repository.CodeChunkRepository;
import com.codeforge.repository.CodeDocumentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.regex.Pattern;

/**
 * Service for processing code files, chunking, and creating embeddings
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class CodeProcessingService {
    
    private final CodeDocumentRepository codeDocumentRepository;
    private final CodeChunkRepository codeChunkRepository;
    
    private static final Set<String> RELEVANT_EXTENSIONS = Set.of(
        "java", "js", "ts", "jsx", "tsx", "py", "go", "rs", "cpp", "c", "h", "hpp",
        "md", "yml", "yaml", "json", "xml", "sql", "sh", "bash", "rb", "php", "cs",
        "kt", "swift", "dart", "r", "scala", "groovy", "lua", "perl", "html", "css", "scss"
    );
    
    private static final Pattern BINARY_PATTERN = Pattern.compile("\\.(png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|pdf|zip|tar|gz|exe|dll|so|dylib|class|jar|war)$");
    
    /**
     * Filter files to keep only relevant source code files
     */
    public Map<String, String> filterRelevantFiles(Map<String, String> files) {
        Map<String, String> filtered = new HashMap<>();
        
        for (Map.Entry<String, String> entry : files.entrySet()) {
            String path = entry.getKey();
            
            // Skip binary files
            if (BINARY_PATTERN.matcher(path.toLowerCase()).find()) {
                continue;
            }
            
            // Skip common ignored directories
            if (path.contains("node_modules/") || path.contains(".git/") || 
                path.contains("build/") || path.contains("dist/") ||
                path.contains("target/") || path.contains(".idea/") ||
                path.contains("venv/") || path.contains("__pycache__/") ||
                path.contains(".vscode/") || path.contains(".gradle/") ||
                path.contains("bin/") || path.contains("obj/")) {
                continue;
            }
            
            // Check if extension is relevant
            String extension = getFileExtension(path);
            if (RELEVANT_EXTENSIONS.contains(extension)) {
                filtered.put(path, entry.getValue());
            }
        }
        
        log.info("Filtered {} relevant files from {} total", filtered.size(), files.size());
        return filtered;
    }
    
    /**
     * Create CodeDocument and CodeChunk entities for a file
     */
    @Transactional
    public CodeDocument createCodeDocumentAndChunks(Project project, String filePath, String content) {
        String language = detectLanguage(filePath);
        
        // Create document
        CodeDocument document = CodeDocument.builder()
            .project(project)
            .filePath(filePath)
            .fullContent(content)
            .language(language)
            .build();
        document = codeDocumentRepository.save(document);
        
        // Create chunks
        List<CodeChunk> chunks = chunkFile(document, content);
        codeChunkRepository.saveAll(chunks);
        
        log.debug("Created document {} with {} chunks", filePath, chunks.size());
        return document;
    }
    
    /**
     * Chunk a file into logical pieces
     */
    public List<CodeChunk> chunkFile(CodeDocument document, String content) {
        List<CodeChunk> chunks = new ArrayList<>();
        String[] lines = content.split("\n");
        
        int chunkSize = 200; // Target lines per chunk
        int startLine = 0;
        int chunkNumber = 0;
        
        while (startLine < lines.length) {
            int endLine = Math.min(startLine + chunkSize, lines.length);
            
            StringBuilder chunkContent = new StringBuilder();
            for (int i = startLine; i < endLine; i++) {
                chunkContent.append(lines[i]).append("\n");
            }
            
            String symbol = extractSymbol(chunkContent.toString(), document.getLanguage());
            
            CodeChunk chunk = CodeChunk.builder()
                .document(document)
                .startLine(startLine + 1) // 1-indexed
                .endLine(endLine)
                .content(chunkContent.toString())
                .symbol(symbol)
                .build();
            
            chunks.add(chunk);
            startLine = endLine;
            chunkNumber++;
        }
        
        return chunks;
    }
    
    /**
     * Extract main symbol from chunk (class name, function name, etc.)
     */
    private String extractSymbol(String content, String language) {
        // Simple pattern matching for common patterns
        String[] lines = content.split("\n");
        
        for (String line : lines) {
            line = line.trim();
            
            // Java/C#/TypeScript class/interface
            if (line.matches(".*\\b(class|interface|enum)\\s+(\\w+).*")) {
                return line.replaceAll(".*\\b(class|interface|enum)\\s+(\\w+).*", "$2");
            }
            
            // Function/method (various languages)
            if (line.matches(".*\\b(function|def|fn|func)\\s+(\\w+).*")) {
                return line.replaceAll(".*\\b(function|def|fn|func)\\s+(\\w+).*", "$2");
            }
            
            // Java method
            if (line.matches(".*\\b(public|private|protected)\\s+.*\\s+(\\w+)\\s*\\(.*")) {
                String[] parts = line.split("\\s+");
                for (int i = 0; i < parts.length - 1; i++) {
                    if (parts[i + 1].contains("(")) {
                        return parts[i + 1].split("\\(")[0];
                    }
                }
            }
        }
        
        return "unknown";
    }
    
    /**
     * Detect programming language from file extension
     */
    private String detectLanguage(String filePath) {
        String extension = getFileExtension(filePath);
        
        return switch (extension) {
            case "java" -> "Java";
            case "js", "jsx" -> "JavaScript";
            case "ts", "tsx" -> "TypeScript";
            case "py" -> "Python";
            case "go" -> "Go";
            case "rs" -> "Rust";
            case "cpp", "cc", "cxx" -> "C++";
            case "c" -> "C";
            case "h", "hpp" -> "C/C++ Header";
            case "cs" -> "C#";
            case "rb" -> "Ruby";
            case "php" -> "PHP";
            case "kt" -> "Kotlin";
            case "swift" -> "Swift";
            case "dart" -> "Dart";
            case "r" -> "R";
            case "scala" -> "Scala";
            case "groovy" -> "Groovy";
            case "lua" -> "Lua";
            case "perl", "pl" -> "Perl";
            case "sh", "bash" -> "Shell";
            case "sql" -> "SQL";
            case "md" -> "Markdown";
            case "json" -> "JSON";
            case "xml" -> "XML";
            case "yml", "yaml" -> "YAML";
            case "html" -> "HTML";
            case "css", "scss" -> "CSS";
            default -> "Unknown";
        };
    }
    
    /**
     * Get file extension from path
     */
    private String getFileExtension(String path) {
        int lastDot = path.lastIndexOf('.');
        if (lastDot > 0 && lastDot < path.length() - 1) {
            return path.substring(lastDot + 1).toLowerCase();
        }
        return "";
    }
}
