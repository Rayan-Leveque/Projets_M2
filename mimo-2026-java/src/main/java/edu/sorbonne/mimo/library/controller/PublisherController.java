package edu.sorbonne.mimo.library.controller;

import edu.sorbonne.mimo.library.entities.Publisher;
import edu.sorbonne.mimo.library.entities.PublisherWriteRequest;
import edu.sorbonne.mimo.library.service.PublisherService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/publishers")
public class PublisherController {

    private static final Logger log = LoggerFactory.getLogger(PublisherController.class);
    private final PublisherService publisherService;

    public PublisherController(PublisherService publisherService) {
        this.publisherService = publisherService;
    }

    @GetMapping
    public List<Publisher> getAllPublishers() {
        return publisherService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Publisher> getPublisher(@PathVariable Long id) {
        return publisherService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Publisher> createPublisher(@RequestBody PublisherWriteRequest request) {
        try {
            Publisher created = publisherService.create(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.error("Publisher '{}' could not be created: {}", request.name(), e.getMessage());
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<Publisher> updatePublisher(@PathVariable Long id,
                                                     @RequestBody PublisherWriteRequest request) {
        try {
            Publisher updated = publisherService.update(id, request);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deletePublisher(@PathVariable Long id) {
        try {
            boolean deleted = publisherService.deleteById(id);
            return deleted ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .build();
        }
    }
}