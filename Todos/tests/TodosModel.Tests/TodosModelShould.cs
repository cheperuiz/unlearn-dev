using System;
using TodosModel;
using Xunit;

namespace TodosModelTests
{
    public class TodosModelShould
    {
        private Todo _sut;

        public TodosModelShould()
        {
            _sut = new Todo("A valid title");
        }


        [Fact]
        public void Todo_NewTodo_ShouldHaveATitle()
        {
            Assert.Throws<ArgumentNullException>(
               () => new Todo()
            );
        }

        [Fact]
        public void Todo_NewTodo_TitleShouldNotBeWhitespace()
        {
            Assert.Throws<ArgumentNullException>(
               () => new Todo("    ")
            );
        }

        [Fact]
        public void Todo_NewTodo_ShouldHaveANewId()
        {
            Assert.NotEqual(Guid.Empty, _sut.Id);
        }

        [Fact]
        public void Todo_Existing_ShouldPreseveId()
        {
            var _id = Guid.NewGuid();
            var _title = "A valid title";
            var todo = new Todo(_title, _id);

            Assert.Equal(_id, todo.Id);
        }

        [Fact]
        public void Todo_NewTodo_ShouldNotBeDone()
        {
            Assert.False(_sut.Done);
        }

        [Fact]
        public void Todo_NewTodo_ShouldBeDoneAfterToggleOnce()
        {
            _sut.Toggle();
            Assert.True(_sut.Done);
        }

        [Fact]
        public void Todo_NewTodo_ShouldNotBeDoneAfterToggleTwice()
        {
            _sut.Toggle();
            _sut.Toggle();

        }
    }
}
