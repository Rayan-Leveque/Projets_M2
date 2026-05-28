package edu.sorbonne.mimo.games.controller;

import edu.sorbonne.mimo.games.entities.Studio;
import edu.sorbonne.mimo.games.entities.StudioWriteRequest;
import edu.sorbonne.mimo.games.entities.Publisher;
import edu.sorbonne.mimo.games.service.StudioService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/studios")
public class StudioController {

    private static final Logger log = LoggerFactory.getLogger(StudioController.class);
    private final StudioService studioService;

    public StudioController(StudioService studioService) {
        this.studioService = studioService;
    }

    @GetMapping
    public List<Studio> getAllStudios() {
        return studioService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Studio> getStudio(@PathVariable Long id) {
        return studioService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/{studioName}/publishers")
    public ResponseEntity<List<Publisher>> getPublishersByStudioName(@PathVariable String studioName) {
        try {
            List<Publisher> publishers = studioService.findPublishersByStudioName(studioName);
            return ResponseEntity.ok(publishers);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<Studio> createStudio(@RequestBody StudioWriteRequest request) {
        try {
            Studio created = studioService.create(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.error("Studio '{}' could not be created: {}", request.name(), e.getMessage());
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<Studio> updateStudio(@PathVariable Long id,
                                               @RequestBody StudioWriteRequest request) {
        try {
            Studio updated = studioService.update(id, request);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteStudio(@PathVariable Long id) {
        boolean deleted = studioService.deleteById(id);
        return deleted ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
}