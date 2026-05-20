package edu.sorbonne.mimo.library.service;

import edu.sorbonne.mimo.library.entities.Publisher;
import edu.sorbonne.mimo.library.entities.PublisherWriteRequest;

import java.util.List;
import java.util.Optional;

public interface PublisherService {

    Publisher create(PublisherWriteRequest request);

    Optional<Publisher> findById(Long id);

    List<Publisher> findAll();

    Publisher update(Long id, PublisherWriteRequest request);

    boolean deleteById(Long id);
}