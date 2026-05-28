package edu.sorbonne.mimo.games.repository;

import edu.sorbonne.mimo.games.entities.db.GameEntity;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface GameRepository extends JpaRepository<GameEntity, String> {

    @Override
    @EntityGraph(attributePaths = {"studio", "publisher"})
    List<GameEntity> findAll();

    @EntityGraph(attributePaths = {"studio", "publisher"})
    Optional<GameEntity> findByCode(String code);

    @EntityGraph(attributePaths = {"studio", "publisher"})
    List<GameEntity> findByGenre(String category);

    @EntityGraph(attributePaths = {"studio", "publisher"})
    List<GameEntity> findByStudio_Name(String studioName);

    @EntityGraph(attributePaths = {"studio", "publisher"})
    List<GameEntity> findByPublisher_Name(String publisherName);

    int countByPublisher_Name(String publisherName);
}