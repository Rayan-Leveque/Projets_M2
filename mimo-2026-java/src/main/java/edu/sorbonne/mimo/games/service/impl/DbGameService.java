package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Game;
import edu.sorbonne.mimo.games.entities.Genre;
import edu.sorbonne.mimo.games.entities.db.StudioEntity;
import edu.sorbonne.mimo.games.entities.db.GameEntity;
import edu.sorbonne.mimo.games.entities.db.PublisherEntity;
import edu.sorbonne.mimo.games.repository.StudioRepository;
import edu.sorbonne.mimo.games.repository.GameRepository;
import edu.sorbonne.mimo.games.repository.PublisherRepository;
import edu.sorbonne.mimo.games.service.GameService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class DbGameService implements GameService {

    private final static Logger log = LoggerFactory.getLogger(DbGameService.class);

    private final GameRepository gameRepository;
    private final StudioRepository studioRepository;
    private final PublisherRepository publisherRepository;

    public DbGameService(GameRepository gameRepository,
                         StudioRepository studioRepository,
                         PublisherRepository publisherRepository) {
        this.gameRepository = gameRepository;
        this.studioRepository = studioRepository;
        this.publisherRepository = publisherRepository;
    }

    @Override
    public List<Game> findAll(String studioName) {
        List<GameEntity> games;
        if(studioName == null || studioName.isEmpty()) {
            games = gameRepository.findAll();
        } else {
            games = gameRepository.findByStudio_Name(studioName);
        }
        return games.stream()
                .map(gameEntity -> gameEntity.toRecord())
                .toList();
    }

    @Override
    public Optional<Game> findByCode(String code) {
        return gameRepository.findByCode(code)
                .map(gameEntity -> gameEntity.toRecord());
    }

    @Override
    public List<Game> findByGenre(Genre category) {
        return gameRepository.findByGenre(category.name())
                .stream()
                .map(gameEntity -> gameEntity.toRecord())
                .toList();
    }

    @Override
    @Transactional
    public void create(Game game) {
        StudioEntity studio = studioRepository.findByName(game.studio())
                .orElseThrow(() -> new IllegalArgumentException(
                        "Studio not found: " + game.studio()));
        PublisherEntity publisher = publisherRepository.findByName(game.publisherName())
                .orElseThrow(() -> new IllegalArgumentException(
                        "Publisher not found: " + game.publisherName()));

        GameEntity gameEntity = GameEntity.fromRecord(game, studio, publisher);
        gameRepository.saveAndFlush(gameEntity);
        log.debug("Created new game: {}", gameEntity.toRecord());
    }

    @Override
    @Transactional
    public Game update(String code, Game updatedGame) {
        if(updatedGame.genre() == null) {
            throw new IllegalArgumentException("Game genre is required");
        }
        GameEntity existing = gameRepository.findByCode(code)
                .orElseThrow(() -> new IllegalArgumentException("Game not found: " + code));

        StudioEntity studio = studioRepository.findByName(updatedGame.studio())
                .orElseThrow(() -> new IllegalArgumentException("Studio not found: " + updatedGame.studio()));
        PublisherEntity publisher = publisherRepository.findByName(updatedGame.publisherName())
                .orElseThrow(() -> new IllegalArgumentException("Publisher not found: " + updatedGame.publisherName()));

        existing.setTitle(updatedGame.title());
        existing.setStudio(studio);
        existing.setPublisher(publisher);
        // Category is stored as String (from Enum), we need the raw name
        existing.setGenre(updatedGame.genre().name());

        gameRepository.saveAndFlush(existing);
        log.debug("Updated game: {}", existing.toRecord());
        return existing.toRecord();
    }

    @Override
    @Transactional
    public boolean deleteByCode(String code) {
        if (gameRepository.existsById(code)) {
            gameRepository.deleteById(code);
            log.debug("Deleted game with code '{}'", code);
            return true;
        }
        return false;
    }
}
