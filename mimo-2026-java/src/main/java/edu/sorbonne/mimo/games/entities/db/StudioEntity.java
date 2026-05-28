package edu.sorbonne.mimo.games.entities.db;

import jakarta.persistence.*;

@Entity
@Table(name = "studios")
public class StudioEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "country")
    private String country;

    @Column(name = "description", length = 500)
    private String description;   // 1‑line description

    public StudioEntity() {}

    public StudioEntity(String name, String country, String description) {
        this.name = name;
        this.country = country;
        this.description = description;
    }

    // getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}