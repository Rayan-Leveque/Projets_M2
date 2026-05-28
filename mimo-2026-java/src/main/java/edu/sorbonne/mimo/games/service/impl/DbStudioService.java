package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Studio;
import edu.sorbonne.mimo.games.entities.StudioWriteRequest;
import edu.sorbonne.mimo.games.entities.Publisher;
import edu.sorbonne.mimo.games.entities.db.StudioEntity;
import edu.sorbonne.mimo.games.entities.db.GameEntity;
import edu.sorbonne.mimo.games.repository.StudioRepository;
import edu.sorbonne.mimo.games.repository.GameRepository;
import edu.sorbonne.mimo.games.repository.PublisherRepository;
import edu.sorbonne.mimo.games.service.StudioService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class DbStudioService implements StudioService {

    private static final Logger log = LoggerFactory.getLogger(DbStudioService.class);
    private final StudioRepository studioRepository;
    private final PublisherRepository publisherRepository;
    private final GameRepository gameRepository;

    public DbStudioService(StudioRepository studioRepository,
                           PublisherRepository publisherRepository,
                           GameRepository gameRepository) {
        this.studioRepository = studioRepository;
        this.publisherRepository = publisherRepository;
        this.gameRepository = gameRepository;
    }

    @Override
    @Transactional
    public Studio create(StudioWriteRequest request) {
        studioRepository.findByName(request.name())
                .ifPresent(studio -> {
                    throw new IllegalArgumentException("Studio already exists");
                });
        StudioEntity entity = new StudioEntity(
                request.name(),
                request.country(),
                request.description());
        StudioEntity saved = studioRepository.saveAndFlush(entity);
        log.debug("Created studio: {}", saved.getId());
        return toRecord(saved);
    }

    @Override
    public Optional<Studio> findById(Long id) {
        return studioRepository.findById(id)
                .map(DbStudioService::toRecord);
    }

    @Override
    public List<Studio> findAll() {
        return studioRepository.findAll()
                .stream()
                .map(DbStudioService::toRecord)
                .toList();
    }

    @Override
    public List<Publisher> findPublishersByStudioName(String studioName) {
        return publisherRepository.findDistinctByStudioName(studioName)
                .stream()
                .map(p -> new Publisher(p.getId(), p.getName(), p.getCountry()))
                .toList();
    }

    @Override
    @Transactional
    public Studio update(Long id, StudioWriteRequest request) {
        StudioEntity existing = studioRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Studio not found: " + id));
        existing.setName(request.name());
        existing.setCountry(request.country());
        existing.setDescription(request.description());
        studioRepository.saveAndFlush(existing);
        log.debug("Updated studio: {}", id);
        return toRecord(existing);
    }

    @Override
    @Transactional
    public boolean deleteById(Long id) {
        Optional<StudioEntity> fromDb = studioRepository.findById(id);
        if (fromDb.isEmpty()) {
            return false;
        }
        String studioName = fromDb.map(db -> db.getName())
                .orElse("");
        List<GameEntity> studioGames = gameRepository.findByStudio_Name(studioName);
        if(!studioGames.isEmpty()) {
            log.warn("Studio has existing games, deleting them");
            gameRepository.deleteAll(studioGames);
        }
        studioRepository.deleteById(id);
        log.debug("Deleted studio: {}", id);
        return true;
    }

    private static Studio toRecord(StudioEntity entity) {
        return new Studio(entity.getId(), entity.getName(), entity.getCountry(), entity.getDescription());
    }
}