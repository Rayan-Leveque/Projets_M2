package edu.sorbonne.mimo.games.service.impl;

import edu.sorbonne.mimo.games.entities.Publisher;
import edu.sorbonne.mimo.games.entities.PublisherWriteRequest;
import edu.sorbonne.mimo.games.entities.db.GameEntity;
import edu.sorbonne.mimo.games.entities.db.PublisherEntity;
import edu.sorbonne.mimo.games.repository.GameRepository;
import edu.sorbonne.mimo.games.repository.PublisherRepository;
import edu.sorbonne.mimo.games.service.PublisherService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class DbPublisherService implements PublisherService {

    private static final Logger log = LoggerFactory.getLogger(DbPublisherService.class);
    private final PublisherRepository publisherRepository;
    private final GameRepository gameRepository;

    public DbPublisherService(PublisherRepository publisherRepository,
                              GameRepository gameRepository) {
        this.publisherRepository = publisherRepository;
        this.gameRepository = gameRepository;
    }

    @Override
    @Transactional
    public Publisher create(PublisherWriteRequest request) {
        publisherRepository.findByName(request.name())
                .ifPresent(publisher -> {
                    throw new IllegalArgumentException("Publisher already exists");
                });
        PublisherEntity entity = new PublisherEntity(request.name(), request.country());
        PublisherEntity saved = publisherRepository.saveAndFlush(entity);
        log.debug("Created publisher: {}", saved.getId());
        return toRecord(saved);
    }

    @Override
    public Optional<Publisher> findById(Long id) {
        return publisherRepository.findById(id)
                .map(DbPublisherService::toRecord);
    }

    @Override
    public List<Publisher> findAll() {
        return publisherRepository.findAll()
                .stream()
                .map(DbPublisherService::toRecord)
                .toList();
    }

    @Override
    @Transactional
    public Publisher update(Long id, PublisherWriteRequest request) {
        PublisherEntity existing = publisherRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Publisher not found: " + id));
        existing.setName(request.name());
        existing.setCountry(request.country());
        publisherRepository.saveAndFlush(existing);
        log.debug("Updated publisher: {}", id);
        return toRecord(existing);
    }

    @Override
    @Transactional
    public boolean deleteById(Long id) {
        Optional<PublisherEntity> fromDb = publisherRepository.findById(id);
        if(fromDb.isEmpty()) {
            return false;
        }
        String publisherName = fromDb.map(db -> db.getName())
                .orElse("");
        int publisherGames = gameRepository.countByPublisher_Name(publisherName);
        if(publisherGames > 0) {
            log.warn("Trying to delete publisher having {} games", publisherGames);
            throw new IllegalArgumentException("Can not delete publisher having games in DB");
        }
        publisherRepository.deleteById(id);
        log.debug("Deleted publisher: {}", id);
        return true;
    }

    private static Publisher toRecord(PublisherEntity entity) {
        return new Publisher(entity.getId(), entity.getName(), entity.getCountry());
    }
}