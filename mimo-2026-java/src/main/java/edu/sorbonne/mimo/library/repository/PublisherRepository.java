package edu.sorbonne.mimo.library.repository;

import edu.sorbonne.mimo.library.entities.db.PublisherEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface PublisherRepository extends JpaRepository<PublisherEntity, Long> {

    Optional<PublisherEntity> findByName(String name);

    @Query("SELECT DISTINCT p FROM PublisherEntity p " +
            "JOIN BookEntity b ON b.publisher = p " +
            "JOIN b.author a " +
            "WHERE a.name = :authorName")
    List<PublisherEntity> findDistinctByAuthorName(@Param("authorName") String authorName);
}