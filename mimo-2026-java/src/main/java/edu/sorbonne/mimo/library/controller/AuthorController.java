package edu.sorbonne.mimo.library.controller;

import edu.sorbonne.mimo.library.entities.Author;
import edu.sorbonne.mimo.library.entities.AuthorWriteRequest;
import edu.sorbonne.mimo.library.entities.Publisher;
import edu.sorbonne.mimo.library.service.AuthorService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/authors")
public class AuthorController {

    private static final Logger log = LoggerFactory.getLogger(AuthorController.class);
    private final AuthorService authorService;

    public AuthorController(AuthorService authorService) {
        this.authorService = authorService;
    }

    @GetMapping
    public List<Author> getAllAuthors() {
        return authorService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Author> getAuthor(@PathVariable Long id) {
        return authorService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/{authorName}/publishers")
    public ResponseEntity<List<Publisher>> getPublishersByAuthorName(@PathVariable String authorName) {
        try {
            List<Publisher> publishers = authorService.findPublishersByAuthorName(authorName);
            return ResponseEntity.ok(publishers);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<Author> createAuthor(@RequestBody AuthorWriteRequest request) {
        try {
            Author created = authorService.create(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.error("Author '{}' could not be created: {}", request.name(), e.getMessage());
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<Author> updateAuthor(@PathVariable Long id,
                                               @RequestBody AuthorWriteRequest request) {
        try {
            Author updated = authorService.update(id, request);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteAuthor(@PathVariable Long id) {
        boolean deleted = authorService.deleteById(id);
        return deleted ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
}