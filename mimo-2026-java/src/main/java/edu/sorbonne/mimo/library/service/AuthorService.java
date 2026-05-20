package edu.sorbonne.mimo.library.service;

import edu.sorbonne.mimo.library.entities.Author;
import edu.sorbonne.mimo.library.entities.AuthorWriteRequest;
import edu.sorbonne.mimo.library.entities.Publisher;

import java.util.List;
import java.util.Optional;

public interface AuthorService {

    Author create(AuthorWriteRequest request);

    Optional<Author> findById(Long id);

    List<Author> findAll();

    List<Publisher> findPublishersByAuthorName(String authorName);

    Author update(Long id, AuthorWriteRequest request);

    boolean deleteById(Long id);
}