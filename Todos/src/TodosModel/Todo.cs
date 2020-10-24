using System;

namespace TodosModel
{
    public class Todo
    {
        public Todo() : this("") { }
        public Todo(string title) : this(title, Guid.NewGuid()) { }
        public Todo(string title, Guid id) =>
            (Title, Id) = (new TitleValue(title), id);

        public TitleValue Title { get; init; }
        public object Id { get; init; }
        public bool Done { get; set; }

        public void Toggle() => Done = !Done;
    }


    public record TitleValue
    {
        public TitleValue(string title)
        {
            Title = title;
        }
        private readonly string? _title;
        public string Title
        {
            get => _title!;
            init => _title =
                !String.IsNullOrWhiteSpace(value)
                ? value
                : throw new ArgumentNullException(nameof(Title));
        }
    }
}
