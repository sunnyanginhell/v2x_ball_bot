// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from v2x_ball_bot_msgs:msg/Ball.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__STRUCT_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__v2x_ball_bot_msgs__msg__Ball __attribute__((deprecated))
#else
# define DEPRECATED__v2x_ball_bot_msgs__msg__Ball __declspec(deprecated)
#endif

namespace v2x_ball_bot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Ball_
{
  using Type = Ball_<ContainerAllocator>;

  explicit Ball_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = "";
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->score = 0.0f;
      this->is_static = false;
    }
  }

  explicit Ball_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init),
    id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = "";
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->score = 0.0f;
      this->is_static = false;
    }
  }

  // field types and members
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _id_type id;
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _z_type =
    float;
  _z_type z;
  using _score_type =
    float;
  _score_type score;
  using _is_static_type =
    bool;
  _is_static_type is_static;

  // setters for named parameter idiom
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__score(
    const float & _arg)
  {
    this->score = _arg;
    return *this;
  }
  Type & set__is_static(
    const bool & _arg)
  {
    this->is_static = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator> *;
  using ConstRawPtr =
    const v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__v2x_ball_bot_msgs__msg__Ball
    std::shared_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__v2x_ball_bot_msgs__msg__Ball
    std::shared_ptr<v2x_ball_bot_msgs::msg::Ball_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Ball_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->id != other.id) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->score != other.score) {
      return false;
    }
    if (this->is_static != other.is_static) {
      return false;
    }
    return true;
  }
  bool operator!=(const Ball_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Ball_

// alias to use template instance with default allocator
using Ball =
  v2x_ball_bot_msgs::msg::Ball_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__STRUCT_HPP_
