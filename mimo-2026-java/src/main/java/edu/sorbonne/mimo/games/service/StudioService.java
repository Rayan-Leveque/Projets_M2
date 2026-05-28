package edu.sorbonne.mimo.games.service;

import edu.sorbonne.mimo.games.entities.Studio;
import edu.sorbonne.mimo.games.entities.StudioWriteRequest;
import edu.sorbonne.mimo.games.entities.Publisher;

import java.util.List;
import java.util.Optional;

public interface StudioService {

    Studio create(StudioWriteRequest request);

    Optional<Studio> findById(Long id);

    List<Studio> findAll();

    List<Publisher> findPublishersByStudioName(String studioName);

    Studio update(Long id, StudioWriteRequest request);

    boolean deleteById(Long id);
}