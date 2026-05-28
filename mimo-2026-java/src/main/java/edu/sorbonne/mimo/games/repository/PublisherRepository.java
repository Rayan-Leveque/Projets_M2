package edu.sorbonne.mimo.games.repository;

import edu.sorbonne.mimo.games.entities.db.PublisherEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface PublisherRepository extends JpaRepository<PublisherEntity, Long> {

    Optional<PublisherEntity> findByName(String name);

    @Query("SELECT DISTINCT p FROM PublisherEntity p " +
            "JOIN GameEntity b ON b.publisher = p " +
            "JOIN b.studio a " +
            "WHERE a.name = :studioName")
    List<PublisherEntity> findDistinctByStudioName(@Param("studioName") String studioName);
}