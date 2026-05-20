package edu.sorbonne.mimo.library.repository;

import edu.sorbonne.mimo.library.entities.db.AuthorEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface AuthorRepository extends JpaRepository<AuthorEntity, Long> {

    Optional<AuthorEntity> findByName(String name);
}