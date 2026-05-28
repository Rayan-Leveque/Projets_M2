package edu.sorbonne.mimo.games.controller;

import edu.sorbonne.mimo.games.entities.Game;
import edu.sorbonne.mimo.games.service.GameService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class GameController {

    private final static Logger log = LoggerFactory.getLogger(GameController.class);

    private final GameService gameService;

    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @GetMapping(value = "/games/{code}")
    public ResponseEntity<Game> getGame(@PathVariable String code) {
        log.debug("Received request to get Game for code '{}'", code);
        Game game = gameService.findByCode(code)
                .orElse(null);
        if (game == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(game);

    }

    @PostMapping("/games")
    public ResponseEntity<Game> createGame(@RequestBody Game game) {
        log.debug("Creating game {}", game);
        gameService.create(game);
        return ResponseEntity.status(HttpStatus.CREATED).body(game);
    }

    @GetMapping(value ="/games")
    public List<Game> getAllGames(@RequestParam(required = false) String studioName) {
        return gameService.findAll(studioName);
    }

    @PutMapping("/games/{code}")
    public ResponseEntity<Game> updateGame(@PathVariable String code, @RequestBody Game game) {
        log.debug("Updating game with code '{}' to {}", code, game);
        try {
            Game updated = gameService.update(code, game);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/games/{code}")
    public ResponseEntity<Void> deleteGame(@PathVariable String code) {
        log.debug("Deleting game with code '{}'", code);
        boolean deleted = gameService.deleteByCode(code);
        if (deleted) {
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
