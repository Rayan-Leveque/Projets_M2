package edu.sorbonne.mimo.library.service.impl;

import edu.sorbonne.mimo.library.entities.Publisher;
import edu.sorbonne.mimo.library.entities.PublisherWriteRequest;
import edu.sorbonne.mimo.library.entities.db.BookEntity;
import edu.sorbonne.mimo.library.entities.db.PublisherEntity;
import edu.sorbonne.mimo.library.repository.BookRepository;
import edu.sorbonne.mimo.library.repository.PublisherRepository;
import edu.sorbonne.mimo.library.service.PublisherService;
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
    private final BookRepository bookRepository;

    public DbPublisherService(PublisherRepository publisherRepository,
                              BookRepository bookRepository) {
        this.publisherRepository = publisherRepository;
        this.bookRepository = bookRepository;
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
        int publisherBooks = bookRepository.countByPublisher_Name(publisherName);
        if(publisherBooks > 0) {
            log.warn("Trying to delete publisher having {} books", publisherBooks);
            throw new IllegalArgumentException("Can not delete publisher having books in DB");
        }
        publisherRepository.deleteById(id);
        log.debug("Deleted publisher: {}", id);
        return true;
    }

    private static Publisher toRecord(PublisherEntity entity) {
        return new Publisher(entity.getId(), entity.getName(), entity.getCountry());
    }
}