package edu.sorbonne.mimo.library.repository;

import edu.sorbonne.mimo.library.entities.db.BookEntity;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface BookRepository extends JpaRepository<BookEntity, String> {

    @Override
    @EntityGraph(attributePaths = {"author", "publisher"})
    List<BookEntity> findAll();

    @EntityGraph(attributePaths = {"author", "publisher"})
    Optional<BookEntity> findByIsbn(String isbn);

    @EntityGraph(attributePaths = {"author", "publisher"})
    List<BookEntity> findByBookCategory(String category);

    @EntityGraph(attributePaths = {"author", "publisher"})
    List<BookEntity> findByAuthor_Name(String authorName);

    @EntityGraph(attributePaths = {"author", "publisher"})
    List<BookEntity> findByPublisher_Name(String publisherName);

    int countByPublisher_Name(String publisherName);
}