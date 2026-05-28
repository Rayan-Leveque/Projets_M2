package edu.sorbonne.mimo.games.repository;

import edu.sorbonne.mimo.games.entities.db.StudioEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface StudioRepository extends JpaRepository<StudioEntity, Long> {

    Optional<StudioEntity> findByName(String name);
}