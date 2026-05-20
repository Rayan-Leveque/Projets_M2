package edu.sorbonne.mimo.library.entities;

public record AuthorWriteRequest(String name,
                                 String country,
                                 String biography) {
}